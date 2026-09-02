# -*- coding: utf-8 -*-
"""
用合肥工业大学官方招生目录 PDF 填充初试科目与招生计划。

来源：《合肥工业大学2023年硕士研究生招生目录》
  http://yjszs.hfut.edu.cn/_upload/article/files/d1/5a/4a20a87c4642b45c6285759ffd2c/
  1e831326-f556-468c-8969-862e53349308.pdf

这份目录除科目外还给出「招生计划 + 计划分配（学院／智能院／工研院）」，
比电子科大那份更细，一并录入 seats。
"""
import json, os

D = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
P = os.path.join(D, "programs.json")
doc = json.load(open(P, encoding="utf-8"))

SRC = ("http://yjszs.hfut.edu.cn/_upload/article/files/d1/5a/4a20a87c4642b45c6285759ffd2c/"
       "1e831326-f556-468c-8969-862e53349308.pdf")
YEAR = "2023"
SCH = "合肥工业大学"

def S(*p): return [{"code": c, "name": n} for c, n in p]
POL = ("101", "思想政治理论")
E1, E2 = ("201", "英语一"), ("204", "英语二")
M1, M2 = ("301", "数学一"), ("302", "数学二")

# (学院关键词, 代码, 业务课, 计划人数, 计划说明)
ROWS = [
 ("电气与自动化工程学院", "085400", (E2, M2, ("834", "自动控制原理")), 10, "非全日制"),
 ("物理学院",             "085400", (E2, M1, ("868", "半导体物理")), None,
  "该目录中物理学院 085400 未单列，科目按同院 085401 的 868 半导体物理，仅供参考"),
 ("微电子学院",           "085401", (E2, M1, ("865", "电子科学与技术综合")), 75,
  "全日制，学院 55 人 + 智能院 20 人"),
 ("物理学院",             "085401", (E2, M1, ("868", "半导体物理")), 15, "全日制，学院 15 人"),
 ("微电子学院",           "085403", (E2, M2, ("865", "电子科学与技术综合")), 25, "非全日制，学院 25 人"),
 ("计算机与信息学院",     "085402", (E2, M1, ("833", "信号分析与处理综合")), 60,
  "全日制，学院 30 + 智能院 29 + 工研院 1"),
 ("计算机与信息学院",     "085404", (E2, M1, ("408", "计算机学科专业基础")), 44,
  "全日制，学院 26 + 智能院 18"),
 ("计算机与信息学院",     "085405", (E2, M2, ("408", "计算机学科专业基础")), 15, "非全日制"),
 ("计算机与信息学院",     "085410", (E2, M1, ("408", "计算机学科专业基础")), 46,
  "全日制，学院 28 + 智能院 18"),
 ("电气与自动化工程学院", "085406", (E2, M2, ("834", "自动控制原理")), 62,
  "全日制，学院 34 + 智能院 28"),
 ("仪器科学与光电工程学院", "085407", (E2, M2, ("854", "仪器技术综合")), 91,
  "全日制，学院 73 + 智能院 15 + 光电院 3"),
 ("仪器科学与光电工程学院", "085408", (E2, M2, ("854", "仪器技术综合")), 15, "非全日制"),
 ("数学学院",             "085412", (E2, M2, ("863", "高级语言程序设计")), 10,
  "非全日制，方向：网络安全与密码／量子计算与安全／应用安全"),
]

filled = 0
for college, code, (en, ma, biz), plan, note in ROWS:
    for r in doc["records"]:
        if r["school"] != SCH or r["code"] != code:
            continue
        if college not in (r.get("college") or ""):
            continue
        if r.get("subjects"):
            continue
        r["subjects"] = S(POL, en, ma, biz)
        if plan:
            seats = r.get("seats") or {}
            seats["plan"] = plan
            seats["note"] = note
            r["seats"] = seats
        srcs = r.get("sources") or []
        if not any(s.get("url") == SRC for s in srcs):
            srcs.append({"url": SRC, "official": True})
        r["sources"] = srcs
        r["dataYear"] = YEAR
        base = r.get("note")
        r["note"] = ((base + "；") if base else "") + \
            f"初试科目取自学校 {YEAR} 年招生目录 PDF 原文" + \
            ("；" + note if note and not plan else "")
        filled += 1
        break

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
print(f"✓ {SCH} 填充 {filled} 条")
print("  该校:", agg[SCH])
print("  全库:", doc["completeness"]["totals"])
