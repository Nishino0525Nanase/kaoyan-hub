# 贡献指南

先说最重要的一条：**这个项目的价值在于数据可核实。**
任何一条新增或修改的数据，都需要能指向一个公开、可访问的来源（官网、官方公告、官方 PDF）。
没有来源的数据，即使是对的，也会被退回。

## 三种最有价值的贡献

### 1. 补充院校

编辑 `src/make_schools.py` 里的 `OTHERS` 列表，追加一行：

```python
("学校全称","城市","省级行政区",["211","双一流"],"研招网URL",["A+学科1","A+学科2"], A类学科总数),
```

然后：

```bash
python3 src/make_schools.py   # 重新生成 data/schools.json
node build.mjs                # 重新生成 index.html
```

要求：

- 研招网 URL 必须**你自己打开验证过**，优先研究生招生网，没有独立招生网就用研究生院官网。
- `aPlus` 只填教育部第四轮学科评估中评为 **A+** 的一级学科，名称用官方写法。
- `aCount` 是 A+、A、A- 三档合计的学科数量。
- 不收录学历提升机构、中外合作办学项目、非全日制专项机构。

### 2. 补充逐校复试分数线 / 报录比

这是目前最缺、也最有用的数据。请**只提交你能给出官方公告链接**的数据。

约定的字段格式（加在 `data/schools.json` 中对应学校对象里，或单独开 `data/lines/<学校拼音>.json`）：

```json
{
  "scores": [
    {
      "year": 2026,
      "major": "081200 计算机科学与技术",
      "college": "计算机学院",
      "line": 350,
      "enrolled": 42,
      "applied": null,
      "source": "https://yzb.example.edu.cn/xxx.html"
    }
  ]
}
```

- `line` 是该专业的复试分数线（学校公布的口径，是院线还是校线请在 PR 里说明）。
- `applied`（报考人数）多数学校不公布，查不到就填 `null`，**不要估算**。
- `source` 必填，且必须是学校官网域名下的页面。

### 3. 纠错

发现链接失效、学校信息过期、分数线抄错，直接开 Issue 或提 PR 都可以。
开 Issue 时请附上：哪一条、错在哪、正确值是什么、来源链接。

## 不会被接受的内容

- 没有来源、或来源是营销号 / 知乎回答 / 微信文章的数据
- 任何形式的付费引流：加微信、进群、报班、卖资料
- 「XX 大学好考 / 不好考」这类主观判断——本项目只放可核实的客观数据
- 直接编辑 `index.html`（它是构建产物，会被覆盖）

## 提交流程

```bash
git checkout -b add-xxx-data
# 改 data/ 或 src/，然后
python3 src/make_schools.py    # 如果动了院校名单
node build.mjs                 # 必跑，index.html 要一起提交
git add -A && git commit -m "data: 补充 XX 大学 2026 年复试线"
git push origin add-xxx-data
```

PR 描述里请写清楚：**改了什么、数据来源是什么**。

## 本地检查

```bash
node build.mjs                                # 构建失败会直接报错（含 JSON 语法错误）
python3 -c "import json;json.load(open('data/schools.json'))"
```

打开 `index.html`，确认院校数、筛选、图表、对比都正常再提交。

感谢你花时间让这份数据更准确一点。

## 2027 招生资料与历史记录

- `data/admissions-2027.json` 保存 2027 年简章、目录与学费快照。按 `year + school + collegeCode + code + studyMode + direction` 标识一条年度记录；专业共用人数只计一次，不向每个方向重复分配。
- `sources` 保存具体官方公告或附件、发布日期、检查日期和核验范围；`content_verified` 只代表已核对声明的范围，`link_verified` 仅核验入口，`access_blocked` 不代表原文失效。学校 `status=published` 表示已收录官方资料，不表示全校字段完整。
- `programs[].evidence` 把字段对应到来源 ID 与 PDF 页码/XLS 行号；`seats.plan` 是目录拟招人数，`seats.exam` 才是明确的统考计划。不得用估计的推免人数相减。学费必须写金额、单位、学习方式与适用范围，不能混用每年和全程。
- 不明字段必须为 JSON `null`，在 `unknownReasons` 说明未查、未公布、访问受阻或不适用。目录复试科目用 `retestSubjects`，复试人数用 `retest`。旧年分数线和录取人数不能带到新年份。
- `programs.json` 是历史聚合产物；应编辑 `programs-base.json` 或 `programs-*-batch*.json`，再运行合并。批次以文件名排序，重复键（学校+代码+名称+学院）保留最早出现的记录，不能靠新增同键批次覆盖旧值。
- `programs-recovered-batch1.json` 仅恢复基线提交中曾直接写入产物的 48 条历史记录，不代表新的官方核验。历史聚合记录数与年度记录数分别统计，不相加宣称覆盖增长。

数据更新后的完整检查：

```bash
python3 src/merge_programs.py
python3 scripts/validate_admissions.py
node build.mjs
```

一起提交源数据、模板与生成产物。打开页面检查院校详情、中大专栏、年度/历史区别及手机横向表格。
