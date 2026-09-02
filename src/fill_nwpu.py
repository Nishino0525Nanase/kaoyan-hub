# -*- coding: utf-8 -*-
"""
西北工业大学：补全 0854 的学院覆盖，并录入学费与住宿政策。

来源：《西北工业大学2025年硕士研究生招生简章》
      https://yzb.nwpu.edu.cn/info/1174/9308.htm
该简章附有各招生单位的学科专业一览表，是官方原文。

说明：初试科目仍留空。学校的招生专业目录页正文只写「见附件」，
附件 PDF 链接未能取到，科目无法核实——按本库规矩不推测，
在 note 中写明空缺原因。
"""
import json, os

D = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
SRC = "https://yzb.nwpu.edu.cn/info/1174/9308.htm"
SCH = "西北工业大学"
PEND = ("学校招生专业目录正文仅写「见附件」，附件 PDF 链接未取到，"
        "初试科目待核实——空缺是还没查到，不是不招")

# ---- programs ----
P = os.path.join(D, "programs.json")
doc = json.load(open(P, encoding="utf-8"))
proto = doc["records"][0]

# 简章一览表里开设 085406 的全部学院（库中已有自动化、航海）
C85406 = ["航空学院", "航天学院", "动力与能源学院", "民航学院", "无人系统技术研究院"]
EXTRA = [(c, "085406", "控制工程") for c in C85406] + [
 ("航空学院", "085410", "人工智能"),
 ("民航学院", "085402", "通信工程（含宽带网络、移动通信等）"),
 ("航海学院", "085401", "新一代电子信息技术（含量子技术等）"),
 ("物理科学与技术学院", "085408", "光电信息工程"),
 ("柔性电子研究院", "085401", "新一代电子信息技术（含量子技术等）"),
 ("柔性电子研究院", "085408", "光电信息工程"),
 ("微电子学院", "085410", "人工智能"),
]

added = 0
for college, code, name in EXTRA:
    if any(r["school"] == SCH and r["code"] == code and college in (r.get("college") or "")
           for r in doc["records"]):
        continue
    rec = {k: ([] if isinstance(proto[k], list) else None) for k in proto}
    rec.update({
        "school": SCH, "track": "ee", "code": code, "name": name,
        "college": college, "degree": "专硕", "dataYear": "2025",
        "tuition": "8000 元/生·年（全日制硕士）",
        "sources": [{"url": SRC, "official": True}],
        "confidence": "official",
        "note": "学院开设情况取自学校 2025 年招生简章的学科专业一览表；" + PEND,
    })
    doc["records"].append(rec)
    added += 1

# 已有的西工大记录补学费并标注科目空缺原因
touched = 0
for r in doc["records"]:
    if r["school"] != SCH:
        continue
    if not r.get("tuition"):
        r["tuition"] = "8000 元/生·年（全日制硕士）"
        touched += 1
    if not r.get("subjects") and PEND not in (r.get("note") or ""):
        r["note"] = ((r["note"] + "；") if r.get("note") else "") + PEND

from collections import defaultdict
agg = defaultdict(lambda: {"n": 0, "sub": 0, "line": 0})
for r in doc["records"]:
    a = agg[r["school"]]; a["n"] += 1
    if r.get("subjects"): a["sub"] += 1
    if r.get("lines") or r.get("line"): a["line"] += 1
doc["completeness"]["bySchool"] = {k: v for k, v in sorted(agg.items())}
doc["completeness"]["totals"] = {
    "records": len(doc["records"]),
    "withSubjects": sum(1 for r in doc["records"] if r.get("subjects")),
    "withLines": sum(1 for r in doc["records"] if r.get("lines") or r.get("line")),
    "withRetestBooks": sum(1 for r in doc["records"] if r.get("retestBooks")),
    "withRetestSubjects": sum(1 for r in doc["records"] if r.get("retestSubjects")),
}
json.dump(doc, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ---- dorms ----
Q = os.path.join(D, "dorms.json")
dm = json.load(open(Q, encoding="utf-8"))
if not any(s["school"] == SCH for s in dm["schools"]):
    dm["schools"].append({
        "school": SCH, "granularity": "policy",
        "audience": "全日制硕士研究生", "confidence": "official", "dataYear": "2025",
        "source": SRC, "sourceLabel": "西北工业大学2025年硕士研究生招生简章",
        "sourcePage": None, "fetched": "2026-09-01",
        "policy": "学校为全日制硕士研究生（学制内）提供住宿",
        "tuition": "全日制硕士 8000 元/生·年",
        "scope": ("简章只写明「提供住宿」这一政策，未公示房型、面积与住宿费标准，"
                  "因此本条 granularity=policy，既不是逐楼栋也不是价格区间。"),
        "campuses": [], "count": 0,
        "stats": {"min": None, "max": None, "bedTypes": []},
    })
    dm["schoolsCovered"] = len(dm["schools"])
    done = {s["school"] for s in dm["schools"]}
    dm["gaps"] = sorted(n for n in dm["gaps"] if n not in done)
    dm["coverage"]["covered"] = len(done)
    dm["note"] += ("　各校公示粒度共三种：building=逐楼栋、range=仅价格区间、"
                   "policy=只公布是否提供住宿而无价格。")
json.dump(dm, open(Q, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

print(f"✓ {SCH} 新增 {added} 条、补学费 {touched} 条")
print("  该校:", agg[SCH])
print("  住宿覆盖:", dm["coverage"]["covered"], "/", dm["coverage"]["total"])
print("  全库:", doc["completeness"]["totals"])
