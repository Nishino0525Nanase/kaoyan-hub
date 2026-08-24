#!/usr/bin/env node
/**
 * 由 index.html 生成 artifact.html —— 用于发布成 Claude Artifact 的变体。
 *
 * 两者的差别只在外壳，不在内容：
 *  1. Artifact 宿主会自己包 <!doctype>/<html>/<head>/<body>，所以要脱掉我们自己的外壳
 *  2. 宿主在根元素上打 data-theme 来控制明暗，我们自己的主题切换按钮会和它打架 —— 去掉
 *  3. <title> 保留（宿主用它做画廊里的名字）
 *
 *   node scripts/make-artifact.mjs
 */
import { readFileSync, writeFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = dirname(dirname(fileURLToPath(import.meta.url)));
let html = readFileSync(join(ROOT, 'index.html'), 'utf8');

const title = '考研择校资料库';   // 画廊里的名字：一个具体名称，不带副标题

// 1. 取出 <head> 里要保留的部分（title + style），丢掉 doctype/meta/link
const style = (html.match(/<style>[\s\S]*?<\/style>/) || [''])[0];

// 2. 取出 body 内容
const body = (html.match(/<body>([\s\S]*)<\/body>/) || [, ''])[1];

// 3. 去掉主题切换按钮 —— Artifact 的明暗由宿主控制
let out = body
  .replace(/<button class="iconbtn" id="themeBtn"[\s\S]*?<\/button>\s*/, '')
  .replace(/const themeBtn = \$\('#themeBtn'\);/, 'const themeBtn = null;')
  .replace(/themeBtn\.onclick = \(\) => \{[\s\S]*?\};\n/, '')
  .replace(/try\{ const t = localStorage\.getItem\('kh-theme'\); if\(t\) applyTheme\(t\); \}catch\(e\)\{\}/,
           '/* 主题由 Artifact 宿主控制，这里不再自行切换 */');

// 4. 宿主换主题时重绘图表（图表颜色是从 CSS 变量读的）
out += `
<script>
/* Artifact 宿主切换明暗时，重绘一次图表——图表颜色从 CSS 变量读取，需要在换肤后重新取值 */
(function(){
  const redraw = () => { try { if (typeof drawAll === 'function') drawAll(); } catch(e){} };
  new MutationObserver(redraw).observe(document.documentElement, { attributes:true, attributeFilter:['data-theme'] });
  matchMedia('(prefers-color-scheme: dark)').addEventListener('change', redraw);
})();
</script>`;

const final = `<title>${title}</title>\n${style}\n${out}`;
writeFileSync(join(ROOT, 'artifact.html'), final);
console.log(`✓ artifact.html 已生成 (${(final.length/1024).toFixed(1)} KB) · 标题：${title}`);
