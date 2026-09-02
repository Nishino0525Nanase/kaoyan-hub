# -*- coding: utf-8 -*-
"""
中山大学 2026 年招生专业目录入库（官方 PDF 全文）。
来源 https://graduate.sysu.edu.cn/zsw/sites/default/files/2025-09/2、中山大学2026年硕士研究生招生学科专业目录.pdf
含初试科目、复试专业课、招生人数，confidence=official。
"""
import json, os
from collections import defaultdict

D = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
P = os.path.join(D, "programs.json")
doc = json.load(open(P, encoding="utf-8"))
proto = doc["records"][0]
SRC = ("https://graduate.sysu.edu.cn/zsw/sites/default/files/2025-09/"
       "2%E3%80%81%E4%B8%AD%E5%B1%B1%E5%A4%A7%E5%AD%A62026%E5%B9%B4%E7%A1%95%E5%A3%AB"
       "%E7%A0%94%E7%A9%B6%E7%94%9F%E6%8B%9B%E7%94%9F%E5%AD%A6%E7%A7%91%E4%B8%93%E4%B8%9A"
       "%E7%9B%AE%E5%BD%95.pdf")

def S(*p): return [{"code": c, "name": n} for c, n in p]
POL = ("101", "思想政治理论")
E1, E2 = ("201", "英语（一）"), ("204", "英语（二）")
M1, M2, M3 = ("301", "数学（一）"), ("302", "数学（二）"), ("303", "数学（三）")

# (院系代码, 学院, 专业代码, 专业名, track, 英, 数, 业务课, 人数, 复试专业课)
R = [
 # 762 电子与信息工程学院（微电子学院）· 广州东校园 · 全院 180 人
 ("762","电子与信息工程学院（微电子学院）","080300","光学工程","ee",E1,M1,("882","光学原理"),18,"7625001 光学工程综合考试A"),
 ("762","电子与信息工程学院（微电子学院）","080900","电子科学与技术","ee",E1,M1,("883","固体物理A"),19,"7625002 半导体器件物理"),
 ("762","电子与信息工程学院（微电子学院）","081000","信息与通信工程","ee",E1,M1,("884","信号与系统"),18,"7625003 电子工程基础综合"),
 ("762","电子与信息工程学院（微电子学院）","085402","通信工程（含宽带网络、移动通信等）","ee",E2,M2,("884","信号与系统"),22,"7625003 电子工程基础综合"),
 ("762","电子与信息工程学院（微电子学院）","085403","集成电路工程","ee",E2,M2,("885","电子技术（数字和模拟）"),81,"7625002 半导体器件物理"),
 ("762","电子与信息工程学院（微电子学院）","085408","光电信息工程","ee",E2,M2,("882","光学原理"),22,"7625004 光学工程综合考试B"),
 # 765 电子与通信工程学院 · 深圳 · 135 人
 ("765","电子与通信工程学院","081000","信息与通信工程","ee",E1,M1,("884","信号与系统"),53,"7655001 电路与信号综合"),
 ("765","电子与通信工程学院","085400","电子信息","ee",E2,M2,("884","信号与系统"),80,"7655001 电路与信号综合"),
 # 754 集成电路学院 · 深圳 · 32 人
 ("754","集成电路学院","085403","集成电路工程","ee",E2,M2,("885","电子技术（数字和模拟）"),20,"7545001 专业基础综合"),
 # 772 微电子科学与技术学院 · 珠海 · 44 人
 ("772","微电子科学与技术学院","080900","电子科学与技术","ee",E1,M1,("883","固体物理A"),2,"7725001 电子工程基础综合 / 7725002 半导体器件物理"),
 ("772","微电子科学与技术学院","085403","集成电路工程","ee",E2,M2,("885","电子技术（数字和模拟）"),34,"7725001 电子工程基础综合 / 7725002 半导体器件物理"),
 # 766 智能工程学院 · 128 人
 ("766","智能工程学院","081100","控制科学与工程","ee",E1,M1,("889","自动控制原理"),24,"7665001 智能技术综合"),
 ("766","智能工程学院","085400","电子信息","ee",E2,M2,("884","信号与系统"),58,"7665001 智能技术综合"),
 # 758 柔性电子学院 · 13 人
 ("758","柔性电子学院","080902","电路与系统","ee",E1,M1,("884","信号与系统"),2,"7585002 电路与信号综合"),
 ("758","柔性电子学院","080903","微电子学与固体电子学","ee",E1,M1,("883","固体物理A"),4,"7585001 半导体器件物理"),
 ("758","柔性电子学院","085401","新一代电子信息技术（含量子技术等）","ee",E2,M2,("884","信号与系统"),4,"7585002 电路与信号综合"),
 ("758","柔性电子学院","085408","光电信息工程","ee",E2,M2,("882","光学原理"),3,"7585001 半导体器件物理"),
 # 771 系统科学与工程学院 · 39 人
 ("771","系统科学与工程学院","081000","信息与通信工程","ee",E1,M1,("884","信号与系统"),7,"7715002 电子工程基础综合"),
 ("771","系统科学与工程学院","085401","新一代电子信息技术（含量子技术等）","ee",E2,M2,("884","信号与系统"),8,"7715003 离散数学与C程序设计"),
 # 767 海洋工程与技术学院
 ("767","海洋工程与技术学院","085400","电子信息","ee",E2,M2,("884","信号与系统"),27,"7675004 数字信号处理"),
 # 724 人工智能学院 / 670 计算机学院（cs 线，一并补齐）
 ("724","人工智能学院","081100","控制科学与工程","ee",E1,M1,("889","自动控制原理"),2,"7245002 智能技术综合"),
 ("724","人工智能学院","085410","人工智能","cs",E2,M2,("408","计算机学科专业基础"),28,"7245001 离散数学与C程序设计"),
 ("670","计算机学院","081200","计算机科学与技术","cs",E1,M1,("408","计算机学科专业基础"),65,"6705001 复试专业课"),
 ("670","计算机学院","085404","计算机技术","cs",E2,M2,("408","计算机学科专业基础"),210,"6705001 复试专业课"),
 ("670","计算机学院","085411","大数据技术与工程","cs",E2,M2,("408","计算机学科专业基础"),40,"6705001 复试专业课"),
 ("757","网络空间安全学院","085412","网络与信息安全","cs",E2,M2,("408","计算机学科专业基础"),23,"7575001 离散数学与C/C++程序设计"),
 ("725","软件工程学院","085405","软件工程","cs",E2,M2,("408","计算机学科专业基础"),37,"7255001 程序设计"),
 ("725","软件工程学院","083500","软件工程","cs",E1,M1,("408","计算机学科专业基础"),11,"7255001 程序设计"),
]

filled = added = 0
for dept, college, code, name, track, en, ma, biz, plan, retest in R:
    hit = next((r for r in doc["records"]
                if r["school"] == "中山大学" and r["code"] == code
                and (college[:6] in (r.get("college") or ""))), None)
    payload = {
        "subjects": S(POL, en, ma, biz), "retestSubjects": retest,
        "dataYear": "2026", "track": track, "college": college,
        "seats": {"plan": plan, "note": f"院系代码 {dept}；2026 年招生专业目录公布的拟招生人数"},
        "sources": [{"url": SRC, "official": True}], "confidence": "official",
        "note": "初试科目、复试专业课与招生人数取自中山大学2026年硕士研究生招生学科专业目录原文",
    }
    if hit:
        hit.update(payload); filled += 1
    else:
        rec = {k: ([] if isinstance(proto[k], list) else None) for k in proto}
        rec.update({"school": "中山大学", "code": code, "name": name,
                    "degree": "专硕" if code.startswith("0854") or code.startswith("0855") else "学硕"})
        rec.update(payload)
        doc["records"].append(rec); added += 1

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
doc["completeness"]["sourceAccess"]["ok"].append(
  "中山大学：全校目录 PDF 在 graduate.sysu.edu.cn/zsw/sites/default/files/ 下，含初试+复试+招生数")
json.dump(doc, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"✓ 中大 更新 {filled} 条、新增 {added} 条 → {dict(agg['中山大学'])}")
print("  全库:", doc["completeness"]["totals"])
