#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""合并 data/programs-base.json 与各 data/programs-*-batch*.json，生成 data/programs.json。
新增数据请加成新的 batch 文件，不要直接改 programs.json（它是合并产物）。"""
import json, os, glob

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, 'data')

DEFAULTS = {
    "college": None, "subjects": [], "lines": [],
    "seats": {"year": None, "plan": None, "tuimian": None},
    "retest": None, "admitted": None, "applied": None, "dataYear": None,
    "tuition": None, "years": None, "changes": None,
    "sources": [], "confidence": "partial", "scale": 500,
}

base = json.load(open(os.path.join(D, 'programs-base.json'), encoding='utf-8'))
records = list(base['records'])
extra_sources = []

for path in sorted(glob.glob(os.path.join(D, 'programs-*-batch*.json'))):
    b = json.load(open(path, encoding='utf-8'))
    records += b['records']
    if b.get('source'):
        extra_sources.append(b['source'])

# 补齐缺省字段 + 去重（学校+专业代码+专业名+学院 唯一）
seen, out = set(), []
for r in records:
    for k, v in DEFAULTS.items():
        r.setdefault(k, json.loads(json.dumps(v)))
    r['lines'] = sorted([l for l in r['lines'] if l.get('score')],
                        key=lambda l: -l['year'])
    key = (r['school'], r['code'], r['name'], r.get('college'))
    if key in seen:
        continue
    seen.add(key)
    out.append(r)

out.sort(key=lambda r: (r['school'], r['track'], r['code'], r['name']))

# MPAcc 是 300 分制，其余 500 分制——写死在记录里，避免图表跨制混比
for r in out:
    r['scale'] = 300 if r['track'] == 'acc' else 500

schools = sorted({r['school'] for r in out})
with_lines = sum(1 for r in out if r['lines'])
with_ratio = sum(1 for r in out if r['retest'] and r['admitted'])

base['records'] = out
from collections import Counter
base['stats'] = {
    "programs": len(out),
    "schools": len(schools),
    "withLines": with_lines,
    "withRetestRatio": with_ratio,
    "withApplied": sum(1 for r in out if r['applied']),
    "byTrack": dict(Counter(r['track'] for r in out)),
}
base['note'] = (
    "逐校逐专业的初试科目、复试线、招录数据。confidence 说明可信度："
    "official=来自学校官网/研招网；secondary=来自考研平台汇总，未经官方核实；partial=部分核实。"
    "查不到的字段一律 null，不估算、不编造。"
    "「复试录取比」= 复试人数 ÷ 拟录取人数，反映进复试后被刷的比例，"
    "不是报录比——报考人数绝大多数学校不公布。"
)
json.dump(base, open(os.path.join(D, 'programs.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print(f"✓ programs.json: {len(out)} 个专业 / {len(schools)} 所学校 · "
      f"有复试线 {with_lines} · 有复试录取比 {with_ratio}")
