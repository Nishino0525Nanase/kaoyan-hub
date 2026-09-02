# -*- coding: utf-8 -*-
"""
用电子科技大学官方招生专业目录 PDF 填充初试/复试科目。

方法上的关键发现：各校招生专业目录的网页入口多是 JS 查询系统（抓不到），
但 PDF 版常直接挂在站点静态目录下（如 xxgkw.uestc.edu.cn/__local/...），
web_fetch 开 pdf_extract_text 就能拿到全文。这条路子可复用到其他学校。

来源：《电子科技大学2024年硕士研究生招生专业目录》
      https://xxgkw.uestc.edu.cn/__local/6/27/77/19A9CC5D5E069F11DAA327CD654_57577346_A4C7C.pdf
该目录同时给出初试科目与复试科目，均为官方原文，confidence=official。

注意：这是 2024 年目录。2026 年计算机/软件方向已改考 408（见 exam-changes），
      涉及的记录在 note 里标注，不把 2024 的科目当成 2026 的。
"""
import json, os

D = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
P = os.path.join(D, "programs.json")
doc = json.load(open(P, encoding="utf-8"))

SRC = ("https://xxgkw.uestc.edu.cn/__local/6/27/77/"
       "19A9CC5D5E069F11DAA327CD654_57577346_A4C7C.pdf")
YEAR = "2024"

def S(*pairs):
    return [{"code": c, "name": n} for c, n in pairs]

POL = ("101", "思想政治理论")
EN1 = ("201", "英语（一）")
M1  = ("301", "数学（一）")
M2  = ("302", "数学（二）")

# (学院, 代码, 名称, 业务课, 复试科目)
ROWS = [
 ("信息与通信工程学院", "085401", "新一代电子信息技术（含量子技术等）",
  ("858", "信号与系统"), "数字逻辑设计"),
 ("电子科学与工程学院", "085401", "新一代电子信息技术（含量子技术等）",
  ("813/858", "01方向 电磁场与电磁波 / 02方向 信号与系统"),
  "01方向 微波技术基础；02方向 电路分析与电子线路"),
 ("深圳高等研究院", "085401", "新一代电子信息技术（含量子技术等）",
  ("813/818", "01方向 电磁场与电磁波 / 02方向 固体物理"),
  "01方向 微波技术基础；02方向 电路分析与电子线路"),
 ("信息与通信工程学院", "085402", "通信工程（含宽带网络、移动通信等）",
  ("858", "信号与系统"), "数字逻辑设计"),
 ("集成电路科学与工程学院", "085403", "集成电路工程",
  ("832/866", "01方向 微电子器件 / 02方向 固体电子学基础"), "电路分析与电子线路"),
 ("深圳高等研究院", "085403", "集成电路工程",
  ("832", "微电子器件"), "电路分析与电子线路"),
 ("自动化工程学院", "085406", "控制工程",
  ("839", "自动控制原理"), "微机原理和数字电路"),
 ("深圳高等研究院", "085406", "控制工程",
  ("839", "自动控制原理"), "数字电路与嵌入式系统"),
 ("资源与环境学院", "085411", "大数据技术与工程",
  ("858", "信号与系统"), "数字信号处理"),
]

def match(r, college, code):
    return (r["school"] == "电子科技大学" and r["code"] == code
            and college in (r.get("college") or ""))

filled = 0
for college, code, name, biz, retest in ROWS:
    for r in doc["records"]:
        if not match(r, college, code):
            continue
        if r.get("subjects"):
            continue
        r["subjects"] = S(POL, EN1, M1, biz)
        r["retestSubjects"] = retest
        srcs = r.get("sources") or []
        if not any(s.get("url") == SRC for s in srcs):
            srcs.append({"url": SRC, "official": True})
        r["sources"] = srcs
        r["confidence"] = "official"
        r["dataYear"] = YEAR
        r["note"] = ((r.get("note") + "；") if r.get("note") else "") + \
            f"初试与复试科目取自学校 {YEAR} 年招生专业目录 PDF 原文"
        filled += 1
        break

# 新增该校目录里有、但库中缺失的 0854 方向
proto = doc["records"][0]
EXTRA = [
 ("信息与通信工程学院", "085400", "电子信息", ("858", "信号与系统"), "数字逻辑设计"),
 ("电子科学与工程学院", "085400", "电子信息",
  ("813/858", "01方向 电磁场与电磁波 / 02方向 信号与系统"),
  "01方向 微波技术基础；02方向 电路分析与电子线路"),
 ("机械与电气工程学院", "085400", "电子信息", ("815", "电路分析基础"), "自动控制原理"),
 ("光电科学与工程学院", "085400", "电子信息",
  ("840/813", "01方向 物理光学 / 02方向 电磁场与电磁波"), "电路分析基础"),
 ("航空航天学院", "085400", "电子信息", ("858", "信号与系统"), "数字逻辑设计"),
 ("物理学院", "085400", "电子信息", ("858", "信号与系统"), "电路分析与电子线路"),
 ("电子科学技术研究院", "085400", "电子信息", ("858", "信号与系统"),
  "01方向 数字逻辑设计；02方向 计算机专业综合；03方向 模拟电路"),
 ("通信抗干扰全国重点实验室", "085400", "电子信息", ("858", "信号与系统"), "通信原理"),
 ("深圳高等研究院", "085400", "电子信息", ("858", "信号与系统"), "通信原理"),
 ("基础与前沿研究院", "085400", "电子信息",
  ("866/840/820", "01方向 固体电子学基础 / 02方向 物理光学 / 03方向 计算机专业基础"),
  "专业英语"),
 ("深圳高等研究院", "085407", "仪器仪表工程", ("858", "信号与系统"), "数字电路"),
 ("自动化工程学院", "085407", "仪器仪表工程",
  ("861", "信号系统与测量基础"), "微机原理和数字电路"),
]

added = 0
for college, code, name, biz, retest in EXTRA:
    if any(match(r, college, code) for r in doc["records"]):
        continue
    rec = {k: ([] if isinstance(proto[k], list) else None) for k in proto}
    rec.update({
        "school": "电子科技大学", "track": "ee", "code": code, "name": name,
        "college": college, "degree": "专硕",
        "subjects": S(POL, EN1, M1, biz),
        "retestSubjects": retest,
        "dataYear": YEAR,
        "sources": [{"url": SRC, "official": True}],
        "confidence": "official",
        "note": f"初试与复试科目取自学校 {YEAR} 年招生专业目录 PDF 原文",
    })
    doc["records"].append(rec)
    added += 1

# 重算完整度
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
print(f"✓ 电子科大 填充 {filled} 条、新增 {added} 条")
print("  该校合计:", agg["电子科技大学"])
print("  全库:", doc["completeness"]["totals"])
