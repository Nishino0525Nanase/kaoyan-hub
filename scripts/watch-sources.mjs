#!/usr/bin/env node
/**
 * 数据源守望：抓取 data/watch-targets.json 里的页面，与上次的内容指纹比对。
 * 变了就输出报告，CI 据此开 Issue 提醒人工核对并更新数据。
 *
 *   node scripts/watch-sources.mjs           # 只跑当月该跑的目标
 *   node scripts/watch-sources.mjs --all     # 忽略季节限制，全跑
 *   node scripts/watch-sources.mjs --json
 *
 * 退出码：0=无变化；1=检测到变化（CI 开 Issue）
 *
 * 【这个脚本能做什么、不能做什么】
 * 能：告诉你某个官网页面变了、页面上出现了「初试科目调整」这类关键词。
 * 不能：自动把变化解析成结构化数据。各校页面结构千差万别，
 *       自动解析必然出错，而这个项目的底线是不出错误数据。
 *       所以它只做预警，取数仍然是人工（或人在 AI 辅助下）完成。
 */
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';

const ROOT = dirname(dirname(fileURLToPath(import.meta.url)));
const DATA = join(ROOT, 'data');
const STATE = join(DATA, '.watch-state.json');
const args = process.argv.slice(2);
const asJson = args.includes('--json');
const runAll = args.includes('--all');

const cfg = JSON.parse(readFileSync(join(DATA, 'watch-targets.json'), 'utf8'));
const state = existsSync(STATE) ? JSON.parse(readFileSync(STATE, 'utf8')) : {};
const month = new Date().getUTCMonth() + 1;

const TIMEOUT_MS = 25000;
const CONCURRENCY = 4;

/** 把 HTML 压成「正文指纹」：去脚本样式标签、去空白、去明显的时间戳数字。
 *  目的是让「页面上挂了个访问计数器」这类噪音不触发误报。 */
function fingerprint(html) {
  const text = html
    .replace(/<script[\s\S]*?<\/script>/gi, ' ')
    .replace(/<style[\s\S]*?<\/style>/gi, ' ')
    .replace(/<!--[\s\S]*?-->/g, ' ')
    .replace(/<[^>]+>/g, ' ')
    .replace(/\d{4}-\d{2}-\d{2}\s*\d{2}:\d{2}(:\d{2})?/g, ' ')  // 精确到时分的时间戳
    .replace(/\s+/g, ' ')
    .trim();
  return { hash: createHash('sha256').update(text).digest('hex').slice(0, 16), text };
}

async function grab(url) {
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), TIMEOUT_MS);
  try {
    const res = await fetch(url, {
      redirect: 'follow', signal: ctrl.signal,
      headers: { 'User-Agent': 'kaoyan-hub-watch/1.0 (+https://github.com/Nishino0525Nanase/kaoyan-hub)' },
    });
    clearTimeout(timer);
    if (!res.ok) return { error: `HTTP ${res.status}` };
    const buf = Buffer.from(await res.arrayBuffer());
    // 教育网站 GB2312/GBK 很常见，优先按声明的字符集解码
    const head = buf.subarray(0, 2048).toString('latin1');
    const m = head.match(/charset=["']?([\w-]+)/i);
    const cs = (m ? m[1] : 'utf-8').toLowerCase();
    let html;
    try {
      html = new TextDecoder(cs === 'gb2312' ? 'gbk' : cs).decode(buf);
    } catch { html = buf.toString('utf8'); }
    return { html };
  } catch (e) {
    clearTimeout(timer);
    return { error: String(e.message || e).slice(0, 120) };
  }
}

/* ---------- 组装待查任务 ---------- */
const jobs = [];
for (const t of cfg.targets) {
  if (!runAll && t.season && !t.season.includes(month)) continue;
  jobs.push({ kind: 'target', id: t.id, name: t.name, url: t.url, why: t.why, keywords: t.keywords });
}
const sw = cfg.schoolWatch;
if (runAll || !sw.season || sw.season.includes(month)) {
  for (const s of sw.sites) {
    jobs.push({ kind: 'school', id: `school:${s.school}`, name: s.school, url: s.url,
                why: '研招网通知页，盯改考类关键词', keywords: sw.keywords });
  }
}

/* ---------- 并发执行 ---------- */
const changes = [], errors = [], unchanged = [];
let cursor = 0;
async function worker() {
  while (cursor < jobs.length) {
    const job = jobs[cursor++];
    const r = await grab(job.url);
    if (r.error) { errors.push({ ...job, error: r.error }); continue; }
    const { hash, text } = fingerprint(r.html);
    const prev = state[job.id];
    const hits = (job.keywords || []).filter(k => text.includes(k));

    if (!prev) {
      // 首次记录，不算变化
      state[job.id] = { hash, seenAt: new Date().toISOString().slice(0, 10), hits };
      unchanged.push({ ...job, note: '首次建立基线' });
    } else if (prev.hash !== hash) {
      const newHits = hits.filter(h => !(prev.hits || []).includes(h));
      changes.push({ ...job, hits, newHits, lastSeen: prev.seenAt });
      state[job.id] = { hash, seenAt: new Date().toISOString().slice(0, 10), hits };
    } else {
      unchanged.push(job);
    }
    if (!asJson) process.stderr.write(r.error ? 'e' : (prev && prev.hash !== hash ? '!' : '.'));
  }
}
await Promise.all(Array.from({ length: CONCURRENCY }, worker));
if (!asJson) process.stderr.write('\n');

mkdirSync(DATA, { recursive: true });
writeFileSync(STATE, JSON.stringify(state, null, 1));

const report = {
  checkedAt: new Date().toISOString().slice(0, 10),
  month, checked: jobs.length,
  changed: changes, errors, unchangedCount: unchanged.length,
};
writeFileSync(join(ROOT, 'watch-report.json'), JSON.stringify(report, null, 1));

if (asJson) {
  console.log(JSON.stringify(report, null, 1));
} else {
  console.log(`本月（${month} 月）应查 ${jobs.length} 个目标：变化 ${changes.length}，抓取失败 ${errors.length}，无变化 ${unchanged.length}`);
  for (const c of changes) {
    console.log(`\n[变化] ${c.name}\n  ${c.url}\n  用途：${c.why}`);
    if (c.newHits.length) console.log(`  ⚠ 新出现关键词：${c.newHits.join('、')}`);
    else if (c.hits.length) console.log(`  页面含关键词：${c.hits.join('、')}`);
  }
  if (errors.length) {
    console.log('\n[抓取失败]（教育网常态，连续多次失败再当回事）');
    errors.forEach(e => console.log(`  ${e.name} ${e.url} — ${e.error}`));
  }
}

process.exit(changes.length ? 1 : 0);
