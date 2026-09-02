# -*- coding: utf-8 -*-
"""
两条官方数据入库：
1) 北京交通大学 2026 自命题改考（学院公告，ai.bjtu.edu.cn）
2) 北京信息科技大学 085406/085410 完整科目（学校招生目录 PDF）
   北信科是上轮新增的 roster 院校，此前零专业记录，这是它的第一批。
"""
import json, os
from collections import defaultdict

D = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

# ---------- 1. 北交大改考 ----------
C = os.path.join(D, "exam-changes.json")
ch = json.load(open(C, encoding="utf-8"))
SRC_BJTU = "https://ai.bjtu.edu.cn/tzgg/rcpytzgg/8f98b5593d0940e6af8b2b6839316380.htm"
new = [{
  "school": "北京交通大学", "track": "ee", "year": 2026, "type": "自命题科目调整",
  "from": "原自动化与智能学院各专业自命题科目",
  "to": "801 自动控制综合（含自动控制原理一 + 数据结构）",
  "scope": "自动化与智能学院 081100 控制科学与工程、082302 交通信息工程及控制、"
           "085401 新一代电子信息技术、085406 控制工程、085410 人工智能",
  "note": "同时调整复试科目：081100/082302/085406 改为 01113 自动控制原理二；"
          "085401 改为 01114 电磁场理论与应用；085410 改为 01115 人工智能基本原理。"
          "初试加考数据结构，对只复习过自控的考生影响较大",
  "source": SRC_BJTU, "official": True}]
have = {(x["school"], x["year"], x.get("to")) for x in ch["changes"]}
add_ch = [x for x in new if (x["school"], x["year"], x.get("to")) not in have]
ch["changes"].extend(add_ch)
ch["updated"] = "2026-09"
json.dump(ch, open(C, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ---------- 2. 北京信息科技大学 ----------
P = os.path.join(D, "programs.json")
doc = json.load(open(P, encoding="utf-8"))
proto = doc["records"][0]
SRC_BISTU = "https://yanjiusheng.bistu.edu.cn/docs/2024-10/3ef3cb5f9e3f47fab3473440b6e662e4.pdf"

def S(*p): return [{"code": c, "name": n} for c, n in p]
BASE = (("101", "思想政治理论"), ("204", "英语（二）"), ("302", "数学（二）"),
        ("803", "自动控制原理"))

ROWS = [
 ("085406", "控制工程", "自动化学院", "00 不区分研究方向", "电路分析", 94, 92, 2),
 ("085410", "人工智能", "自动化学院", "01 自主智能控制", "电路与电子技术", 20, 18, 2),
]
added = 0
for code, name, college, direction, retest, plan, exam, tm in ROWS:
    if any(r["school"] == "北京信息科技大学" and r["code"] == code for r in doc["records"]):
        continue
    rec = {k: ([] if isinstance(proto[k], list) else None) for k in proto}
    rec.update({
        "school": "北京信息科技大学", "track": "ee", "code": code, "name": name,
        "college": college, "degree": "专硕", "dataYear": "2025",
        "subjects": S(*BASE), "retestSubjects": retest,
        "seats": {"plan": plan, "exam": exam, "tuimian": tm,
                  "note": f"拟招 {plan}，其中统考 {exam}、推免 {tm}"},
        "sources": [{"url": SRC_BISTU, "official": True}],
        "confidence": "official",
        "note": f"研究方向 {direction}；初试、复试科目与招生数取自学校 2025 年招生专业目录 PDF 原文",
    })
    doc["records"].append(rec)
    added += 1

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
# 记录数据源可达性经验，供后续（含他人 PR）参考
doc["completeness"]["sourceAccess"] = {
  "note": "各校招生目录的可达性差异很大，逐所试出来的结论：",
  "ok": ["电子科技大学：目录 PDF 挂在 xxgkw.uestc.edu.cn/__local/ 下，可直接取",
         "合肥工业大学：PDF 在 yjszs.hfut.edu.cn/_upload/ 下，含科目与招生计划",
         "南京大学电科院：网页正文是图片，但附件 PDF 可取（复试参考书目）",
         "北京信息科技大学：PDF 在 yanjiusheng.bistu.edu.cn/docs/ 下"],
  "blocked": ["西北工业大学：目录页正文只写「见附件」，附件链接提取不到",
              "西南交通大学：整站为 vatuu 查询系统，表格由 JS 填充",
              "北京科技大学：逐专业页面把目录做成 image.png，无文字层"],
}
json.dump(doc, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"✓ 改考 +{len(add_ch)} 条（共 {len(ch['changes'])}）")
print(f"✓ 北信科 +{added} 条 → {dict(agg['北京信息科技大学'])}")
print("  全库:", doc["completeness"]["totals"])
