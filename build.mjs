#!/usr/bin/env node
/**
 * 把 data/*.json 注入 src/template.html，生成根目录的 index.html。
 * 零依赖，Node 16+ 即可运行：  node build.mjs
 */
import { readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const ROOT = dirname(fileURLToPath(import.meta.url));
const REPO_URL = process.env.REPO_URL || 'https://github.com/Nishino0525Nanase/kaoyan-hub';

const read = p => readFileSync(join(ROOT, p), 'utf8');

// JSON 会被塞进 <script type="application/json">，必须切断 </script> 与注释序列
const inject = obj => JSON.stringify(obj)
  .replace(/</g, '\\u003c')
  .replace(/>/g, '\\u003e')
  .replace(/\u2028/g, '\\u2028')
  .replace(/\u2029/g, '\\u2029')

const files = {
  __DATA_SCHOOLS__: 'data/schools.json',
  __DATA_LINES__:   'data/national-lines-2026.json',
  __DATA_HISTORY__: 'data/national-lines-history.json',
  __DATA_RES__:     'data/resources.json',
  __DATA_PROGRAMS__:'data/programs.json',
  __DATA_CHANGES__: 'data/exam-changes.json',
  __DATA_TRACKS__:  'data/track-catalog.json',
  __DATA_QUOTA__:   'data/quota-retest.json',
  __DATA_ADV__:     'data/advisors.json',
  __DATA_DORM__:    'data/dorms.json',
  __DATA_SYSU__:    'data/sysu.json',
  __DATA_NJU__:     'data/nju.json',
};

/* ---- 数据新鲜度：构建时算一次，页面直接显示「这块数据多久没动了」---- */
const NOW = new Date();
const Y = NOW.getUTCFullYear(), M = NOW.getUTCMonth() + 1;
const monthsSince = (ym) => {
  if (!ym) return null;
  const [y, m] = String(ym).split('-').map(Number);
  return (Y - y) * 12 + (M - (m || 1));
};
const grade = (mo) => mo == null ? 'unknown' : mo <= 6 ? 'fresh' : mo <= 12 ? 'aging' : 'stale';

function freshness() {
  const rd = (f) => JSON.parse(read(`data/${f}`));
  const progs = rd('programs.json');
  const years = progs.records.flatMap(r => (r.lines || []).map(l => l.year)).filter(Boolean);
  const newestLine = years.length ? Math.max(...years) : null;
  const staleRecords = progs.records.filter(r => {
    const y = (r.lines || [])[0]?.year || r.dataYear;
    return y && y < Y - 1;
  }).length;

  const sets = [
    { key: '国家线',        file: 'national-lines-2026.json',    updated: '2026-02', note: '每年 2—3 月教育部发布新一年' },
    { key: '历年国家线趋势', file: 'national-lines-history.json', updated: '2026-02', note: '随每年国家线一起更新' },
    { key: '院校档案',      file: 'schools.json',                updated: rd('schools.json').updated, note: '研招网链接、层次、学科评估' },
    { key: '改考预警',      file: 'exam-changes.json',           updated: rd('exam-changes.json').updated, note: '每年 4—9 月是各校发布改考公告的高峰' },
    { key: '逐专业数据',    file: 'programs.json',               updated: progs.updated, note: `最新收录到 ${newestLine || '—'} 年复试线` },
    { key: '方向目录',      file: 'track-catalog.json',          updated: rd('track-catalog.json').updated, note: '0854 二级目录、MPAcc 说明' },
    { key: '导师名录',      file: 'advisors.json',               updated: rd('advisors.json').updated, note: '各学院官网师资页，随学院更新而变动' },
    { key: '校区住宿',      file: 'dorms.json',                  updated: rd('dorms.json').updated, note: '学校信息公开网每年 7 月前后公示新学年标准' },
    { key: '中大专栏',      file: 'sysu.json',                   updated: rd('sysu.json').updated, note: '聚合本库中大数据 + 校级政策，随学校发布更新' },
  ].map(x => {
    const mo = monthsSince(x.updated);
    return { ...x, monthsAgo: mo, grade: grade(mo) };
  });

  // 季节提醒：现在这个月，考研人该盯什么
  const CAL = {
    2: '国家线通常本月或下月发布，盯研招网',
    3: '国家线发布 + 各校复试线陆续公布；调剂系统开放',
    4: '调剂高峰；各校开始发布下一年改考公告',
    5: '改考公告高峰，本库的改考预警最该更新',
    6: '改考公告高峰',
    7: '改考公告高峰；暑期强化',
    8: '考试大纲发布；招生简章陆续出',
    9: '招生专业目录发布（初试科目的权威来源）；预报名',
    10: '正式报名',
    11: '现场确认 / 网上确认',
    12: '初试',
    1: '初试成绩陆续公布',
  };

  return {
    builtAt: `${Y}-${String(M).padStart(2, '0')}`,
    sets,
    staleRecords,
    totalRecords: progs.records.length,
    seasonHint: CAL[M] || null,
    month: M,
  };
}

const FRESH = freshness();

let html = read('src/template.html');
html = html.replaceAll('__DATA_FRESH__', inject(FRESH));
for (const [token, path] of Object.entries(files)) {
  const parsed = JSON.parse(read(path));           // 顺带校验 JSON 合法性
  html = html.replaceAll(token, inject(parsed));
}
html = html.replaceAll('__REPO_URL__', REPO_URL);

const left = html.match(/__DATA_[A-Z_]+__|__REPO_URL__/g);
if (left) { console.error('未替换的占位符:', [...new Set(left)]); process.exit(1); }

writeFileSync(join(ROOT, 'index.html'), html);
console.log(`✓ index.html 已生成 (${(html.length / 1024).toFixed(1)} KB)`);
