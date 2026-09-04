# -*- coding: utf-8 -*-
"""
1) 补中大 2026 目录里上一轮漏掉的条目（085409 生物医学工程三个方向、083100、
   以及三处「仅招收推免生」的 140100 集成电路科学与工程）。
   数据来自同一份官方 PDF，无需再抓。
2) 记录华南理工 2027 初试自命题调整通知的存在。
   注意：华工研招网 robots 禁止抓取、招生目录为查询系统，
   通知正文取不到，因此 from/to 一律 null，只登记「有这么一份通知 + 链接」，
   不编造调整内容。
"""
import json, os
from collections import defaultdict

D = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
SYSU_SRC = ("https://graduate.sysu.edu.cn/zsw/sites/default/files/2025-09/"
  "2%E3%80%81%E4%B8%AD%E5%B1%B1%E5%A4%A7%E5%AD%A62026%E5%B9%B4%E7%A1%95%E5%A3%AB"
  "%E7%A0%94%E7%A9%B6%E7%94%9F%E6%8B%9B%E7%94%9F%E5%AD%A6%E7%A7%91%E4%B8%93%E4%B8%9A%E7%9B%AE%E5%BD%95.pdf")

P = os.path.join(D, "programs.json")
doc = json.load(open(P, encoding="utf-8"))
proto = doc["records"][0]
def S(*p): return [{"code": c, "name": n} for c, n in p]
POL = ("101", "思想政治理论")
E1, E2 = ("201", "英语（一）"), ("204", "英语（二）")
M1, M2 = ("301", "数学（一）"), ("302", "数学（二）")
RB = ("7695001 电路原理、数字电路与模拟电路综合 / 7695006 生物医学电子与传感器 / "
      "7695005 数据结构与算法设计 / 7695004 细胞生物学 / 7695002 高分子化学与物理")

NEW = [
 # 769 生物医学工程学院 —— 085409 分三个方向，业务课不同，02 方向考信号与系统
 ("769","生物医学工程学院","085409","生物医学工程（01 生物医学材料）","ee",E1,M1,("894","生物化学（A）"),7,RB,"专硕",False),
 ("769","生物医学工程学院","085409","生物医学工程（02 生物医学传感）","ee",E1,M1,("884","信号与系统"),6,RB,"专硕",False),
 ("769","生物医学工程学院","085409","生物医学工程（03 医疗仪器）","ee",E1,M1,("894","生物化学（A）"),9,RB,"专硕",False),
 ("769","生物医学工程学院","083100","生物医学工程","ee",E2,M2,("884","信号与系统"),22,RB,"学硕",False),
 ("769","生物医学工程学院","086001","生物技术与工程","ee",E2,M2,("894","生物化学（A）"),28,RB,"专硕",False),
 # 三处 140100 集成电路科学与工程：全部仅招推免，统考生报不了
 ("754","集成电路学院","140100","集成电路科学与工程","ee",None,None,None,12,None,"学硕",True),
 ("772","微电子科学与技术学院","140100","集成电路科学与工程","ee",None,None,None,8,None,"学硕",True),
 ("765","电子与通信工程学院","140100","集成电路科学与工程","ee",None,None,None,2,None,"学硕",True),
 ("773","遥感科学与技术学院","140400","遥感科学与技术","ee",None,None,None,10,None,"学硕",True),
]
added = 0
for dept, col, code, name, track, en, ma, biz, plan, rt, deg, tuimian_only in NEW:
    if any(r["school"]=="中山大学" and r["code"]==code and col[:6] in (r.get("college") or "")
           and (r.get("name") or "")==name for r in doc["records"]):
        continue
    rec = {k: ([] if isinstance(proto[k], list) else None) for k in proto}
    rec.update({
      "school":"中山大学","track":track,"code":code,"name":name,"college":col,
      "degree":deg,"dataYear":"2026",
      "subjects": S(POL,en,ma,biz) if biz else [],
      "retestSubjects": rt,
      "seats": {"plan": plan, "note": f"院系代码 {dept}；2026 年目录拟招生人数"},
      "sources":[{"url":SYSU_SRC,"official":True}],"confidence":"official",
      "note": ("目录明确标注「仅招收推免生」，统考生无法报考——这是确实不招，不是数据缺失"
               if tuimian_only else
               "初试科目、复试专业课与招生人数取自中山大学2026年招生专业目录原文"),
      "tuimianOnly": tuimian_only,
    })
    doc["records"].append(rec); added += 1

agg = defaultdict(lambda: {"n":0,"sub":0,"line":0})
for r in doc["records"]:
    a=agg[r["school"]]; a["n"]+=1
    if r.get("subjects"): a["sub"]+=1
    if r.get("lines") or r.get("line"): a["line"]+=1
doc["completeness"]["bySchool"]={k:v for k,v in sorted(agg.items())}
doc["completeness"]["totals"]={
 "records":len(doc["records"]),
 "withSubjects":sum(1 for r in doc["records"] if r.get("subjects")),
 "withLines":sum(1 for r in doc["records"] if r.get("lines") or r.get("line")),
 "withRetestBooks":sum(1 for r in doc["records"] if r.get("retestBooks")),
 "withRetestSubjects":sum(1 for r in doc["records"] if r.get("retestSubjects")),
 "tuimianOnly":sum(1 for r in doc["records"] if r.get("tuimianOnly")),
}
doc["completeness"]["sourceAccess"]["blocked"].append(
 "华南理工大学：研招网 robots 禁止自动访问，招生目录为 yanzhao.scut.edu.cn 查询系统，两条路都不通")
json.dump(doc, open(P,"w",encoding="utf-8"), ensure_ascii=False, indent=1)

# 华工 2027 自命题调整通知
C = os.path.join(D, "exam-changes.json")
ch = json.load(open(C, encoding="utf-8"))
SCUT = "https://yz.scut.edu.cn/sszs/list.htm"
item = {"school":"华南理工大学","track":"ee","year":2027,"type":"自命题科目调整（详情待核实）",
 "from":None,"to":None,
 "scope":"自动化科学与工程学院、物理与光电学院、吴贤铭智能工程学院部分专业",
 "note":("学校 2026-06-22 发布《关于自动化科学与工程学院、物理与光电学院和吴贤铭智能工程学院"
         "部分专业2027年初试自命题科目调整的通知》。该校研招网 robots 禁止自动访问，"
         "通知正文未能取到，具体调整内容待考生自行查阅原文——本条只登记「存在这份通知」，"
         "不推测调整内容。2027 年报考上述三个学院务必点开原文核对"),
 "source":SCUT,"official":True}
if not any(x["school"]=="华南理工大学" and x.get("year")==2027 for x in ch["changes"]):
    ch["changes"].append(item)
ch["updated"]="2026-09"
json.dump(ch, open(C,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"✓ 中大 +{added} 条 → {dict(agg['中山大学'])}")
print(f"✓ 改考 {len(ch['changes'])} 条（含华工 2027 预警）")
print("  全库:", doc["completeness"]["totals"])
