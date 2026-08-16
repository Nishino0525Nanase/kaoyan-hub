#!/usr/bin/env node
/**
 * 把 data/*.json 注入 src/template.html，生成根目录的 index.html。
 * 零依赖，Node 16+ 即可运行：  node build.mjs
 */
import { readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const ROOT = dirname(fileURLToPath(import.meta.url));
const REPO_URL = process.env.REPO_URL || 'https://github.com/OWNER/kaoyan-schools';

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
};

let html = read('src/template.html');
for (const [token, path] of Object.entries(files)) {
  const parsed = JSON.parse(read(path));           // 顺带校验 JSON 合法性
  html = html.replaceAll(token, inject(parsed));
}
html = html.replaceAll('__REPO_URL__', REPO_URL);

const left = html.match(/__DATA_[A-Z_]+__|__REPO_URL__/g);
if (left) { console.error('未替换的占位符:', [...new Set(left)]); process.exit(1); }

writeFileSync(join(ROOT, 'index.html'), html);
console.log(`✓ index.html 已生成 (${(html.length / 1024).toFixed(1)} KB)`);
