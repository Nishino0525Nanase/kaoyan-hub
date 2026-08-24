#!/usr/bin/env node
/**
 * 链接体检：把 data/*.json 里所有 URL 拉一遍，报告失效的。
 * 零依赖，Node 18+ 自带 fetch。
 *
 *   node scripts/check-links.mjs            # 全量检查，人读的输出
 *   node scripts/check-links.mjs --json     # 输出 JSON，给 CI 用
 *   node scripts/check-links.mjs --only=schools   # 只查某个文件
 *
 * 退出码：0=全通过或只有警告；1=有确定失效的链接（CI 据此开 Issue）
 */
import { readFileSync, readdirSync, writeFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = dirname(dirname(fileURLToPath(import.meta.url)));
const DATA = join(ROOT, 'data');
const args = process.argv.slice(2);
const asJson = args.includes('--json');
const only = (args.find(a => a.startsWith('--only=')) || '').split('=')[1];

const CONCURRENCY = 6;      // 别把人家学校官网打挂了
const TIMEOUT_MS = 20000;
const RETRIES = 2;

/* ---------- 1. 从所有 JSON 里递归收集 URL ---------- */
const urls = new Map();     // url -> [{file, path}]
function walk(node, file, path) {
  if (node == null) return;
  if (typeof node === 'string') {
    if (/^https?:\/\//.test(node)) {
      if (!urls.has(node)) urls.set(node, []);
      urls.get(node).push({ file, path });
    }
    return;
  }
  if (Array.isArray(node)) return node.forEach((v, i) => walk(v, file, `${path}[${i}]`));
  if (typeof node === 'object') {
    for (const [k, v] of Object.entries(node)) walk(v, file, path ? `${path}.${k}` : k);
  }
}

const files = readdirSync(DATA).filter(f => f.endsWith('.json') && !f.startsWith('.'));
for (const f of files) {
  if (only && !f.includes(only)) continue;
  walk(JSON.parse(readFileSync(join(DATA, f), 'utf8')), f, '');
}

/* ---------- 2. 逐个探测 ---------- */
async function probe(url) {
  for (let attempt = 0; attempt <= RETRIES; attempt++) {
    const ctrl = new AbortController();
    const timer = setTimeout(() => ctrl.abort(), TIMEOUT_MS);
    try {
      // 先 HEAD，很多教育网站不支持，失败再 GET
      let res = await fetch(url, {
        method: 'HEAD', redirect: 'follow', signal: ctrl.signal,
        headers: { 'User-Agent': 'kaoyan-hub-linkcheck/1.0 (+https://github.com/Nishino0525Nanase/kaoyan-hub)' },
      });
      if (res.status === 405 || res.status === 501 || res.status === 403) {
        res = await fetch(url, {
          method: 'GET', redirect: 'follow', signal: ctrl.signal,
          headers: { 'User-Agent': 'kaoyan-hub-linkcheck/1.0' },
        });
      }
      clearTimeout(timer);
      return { status: res.status, finalUrl: res.url };
    } catch (e) {
      clearTimeout(timer);
      if (attempt === RETRIES) return { status: 0, error: String(e.message || e).slice(0, 120) };
      await new Promise(r => setTimeout(r, 1500 * (attempt + 1)));
    }
  }
}

const list = [...urls.keys()];
const results = [];
let cursor = 0;
async function worker() {
  while (cursor < list.length) {
    const url = list[cursor++];
    const r = await probe(url);
    results.push({ url, ...r, refs: urls.get(url) });
    if (!asJson) process.stderr.write('.');
  }
}
await Promise.all(Array.from({ length: CONCURRENCY }, worker));
if (!asJson) process.stderr.write('\n');

/* ---------- 3. 分类 ---------- */
// 404/410 = 确定失效。0（网络错误/超时）= 存疑，教育网常年不稳定，不当失败。
const dead = results.filter(r => r.status === 404 || r.status === 410);
const suspect = results.filter(r => r.status === 0 || (r.status >= 500 && r.status < 600));
const ok = results.filter(r => r.status >= 200 && r.status < 400);
const other = results.filter(r => !dead.includes(r) && !suspect.includes(r) && !ok.includes(r));

const report = {
  checkedAt: new Date().toISOString().slice(0, 10),
  total: results.length,
  ok: ok.length,
  dead: dead.map(r => ({ url: r.url, status: r.status, refs: r.refs })),
  suspect: suspect.map(r => ({ url: r.url, status: r.status, error: r.error, refs: r.refs })),
  other: other.map(r => ({ url: r.url, status: r.status, refs: r.refs })),
};

if (asJson) {
  console.log(JSON.stringify(report, null, 1));
} else {
  console.log(`共 ${report.total} 条链接：正常 ${ok.length}，失效 ${dead.length}，存疑 ${suspect.length}，其他 ${other.length}`);
  if (dead.length) {
    console.log('\n== 确定失效（404/410）==');
    for (const d of dead) {
      console.log(`  ${d.url}`);
      d.refs.slice(0, 3).forEach(x => console.log(`      ← ${x.file} : ${x.path}`));
    }
  }
  if (suspect.length) {
    console.log('\n== 存疑（超时/5xx，教育网常见，不一定真失效）==');
    suspect.slice(0, 20).forEach(d => console.log(`  [${d.status || 'ERR'}] ${d.url} ${d.error || ''}`));
    if (suspect.length > 20) console.log(`  …另有 ${suspect.length - 20} 条未列出`);
  }
}

writeFileSync(join(ROOT, 'link-report.json'), JSON.stringify(report, null, 1));
process.exit(dead.length ? 1 : 0);
