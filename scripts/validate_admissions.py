#!/usr/bin/env python3
"""检查年度招生资料的年份、身份、官方证据及人数/空值口径。仅用标准库。"""
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / 'data/admissions-2027.json').read_text(encoding='utf-8'))
sources = {s['id']: s for s in data['sources']}
assert len(sources) == len(data['sources']), '重复来源 ID'
school_names = {s['name'] for s in json.loads((ROOT/'data/schools.json').read_text(encoding='utf-8'))['schools']}
allowed = {'content_verified', 'link_verified', 'access_blocked'}
for s in sources.values():
    assert s['year'] == data['year'] == 2027
    assert s['school'] in school_names and s['official'] is True
    assert urlparse(s['url']).hostname.endswith('.edu.cn'), s['url']
    assert s['verification'] in allowed and s['verificationScope']
    assert s['checkedAt'] <= data['updated']

seen = set()
for p in data['programs']:
    key = (p['year'],p['school'],p['collegeCode'],p['code'],p['studyMode'],p['direction'])
    assert key not in seen, key
    seen.add(key)
    assert p['year'] == 2027 and p['school'] in school_names
    assert len(p['subjects']) == (2 if p['code']=='125300' else 4), key
    assert all(s['code'] and s['name'] for s in p['subjects']), key
    for value in p['seats'].values():
        assert not isinstance(value, str) or value == p['seats']['basis'], key
    for field in ['line','applied','retest','admitted','years']:
        assert field in p, (key, field)
        assert p[field] is None or isinstance(p[field],(int,float)), (key,field)
        if p[field] is None: assert p['unknownReasons'].get(field), (key,field)
    for field in ['plan','tuimian','exam']:
        assert field in p['seats']
        v=p['seats'][field]
        assert v is None or (type(v) is int and v >= 0), (key,field)
        if v is None: assert p['unknownReasons'].get('seats.'+field), (key,field)
    if p['tuition']['amount'] is None:
        assert p['unknownReasons'].get('tuition.amount'), key
    else:
        assert p['tuition']['amount'] > 0 and p['tuition']['unit'] in {'元/生·学年','元/生·全程'}, key
    if p['retestSubjects'] is None: assert p['unknownReasons'].get('retestSubjects')
    for e in p['evidence']:
        s=sources[e['sourceId']]
        assert s['school']==p['school'] and s['verification']=='content_verified' and e['locator'], key

for s in data['schools']:
    assert s['school'] in school_names and s['year']==2027
    for sid in s['sourceIds']: assert sources[sid]['school']==s['school']
    for p in s['policies'] + s['feeRules']:
        assert sources[p['sourceId']]['school']==s['school']
        assert sources[p['sourceId']]['verification']=='content_verified'

# 回归：这些口径一旦混淆，会直接误导选校和报名。
sysu=[p for p in data['programs'] if p['school']=='中山大学']
assert len(sysu)==12
assert all(p['code']!='085403' for p in sysu)
assert [(p['seats']['plan'],p['retestSubjects'][0]['code']) for p in sysu if p['collegeCode']=='767']==[(50,'7675008')]
assert all(p['seats']['exam'] is None and p['seats']['tuimian'] is None for p in sysu)
hdu_ai=next(p for p in data['programs'] if p['school']=='杭州电子科技大学' and p['code']=='085410' and p['studyMode']=='非全日制')
assert hdu_ai['tuition']['amount'] is None
sjtu=[p for p in data['programs'] if p['school']=='上海交通大学']
assert all(p['seats']['plan'] is None for p in sjtu), '不得把学院总计划复制到方向'
assert all(p['line'] is None and p['admitted'] is None for p in data['programs']), '不得将历史结果平移到 2027'
print(f"✓ 2027 招生资料：{len(data['schools'])} 所院校检查记录，{len(sources)} 个官方来源，{len(seen)} 条年度专业/方向记录")
