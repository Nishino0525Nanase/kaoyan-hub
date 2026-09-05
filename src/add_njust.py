# -*- coding: utf-8 -*-
"""
南京理工大学 085406 等（官方研究生院目录 PDF），并登记「南大 085406 存疑」。
"""
import json, os
from collections import defaultdict
D = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
P = os.path.join(D, "programs.json")
doc = json.load(open(P, encoding="utf-8"))
proto = doc["records"][0]
SRC = ("https://gs.njust.edu.cn/_upload/article/files/71/53/7b332b0d44d18a118926c218e057/"
       "f3928315-cf11-4ed7-8910-9c5939ca1857.pdf")
def S(*p): return [{"code": c, "name": n} for c, n in p]
B = (("101","思想政治理论"), ("204","英语二"), ("302","数学二"))

ROWS = [
 ("085406","控制工程","自动化学院",("873","自动控制理论"),"微机原理与接口技术",
  "全日制 01 不区分研究方向；非全日制 F1 方向可接收单独考试考生"),
 ("085801","电气工程","自动化学院",("837","电路"),"电力电子技术",
  "全日制 01 不区分研究方向；含非全日制 F1"),
 ("086100","交通运输","自动化学院",("873","自动控制理论"),"智能交通控制","全日制 01 不区分研究方向"),
]
added = 0
for code,name,col,biz,retest,note in ROWS:
    if any(r["school"]=="南京理工大学" and r["code"]==code and col in (r.get("college") or "")
           for r in doc["records"]): continue
    rec = {k: ([] if isinstance(proto[k], list) else None) for k in proto}
    rec.update({"school":"南京理工大学","track":"ee","code":code,"name":name,"college":col,
      "degree":"专硕","dataYear":"2025","subjects":S(*B,biz),"retestSubjects":retest,
      "sources":[{"url":SRC,"official":True}],"confidence":"official",
      "note":note+"；初试与复试科目取自学校 2025 年招生专业目录 PDF 原文"})
    doc["records"].append(rec); added += 1

# 登记南大 085406 存疑，避免下次重复查
doc["completeness"]["verifyNeeded"] = doc["completeness"].get("verifyNeeded", [])
item = {"school":"南京大学","code":"085406","name":"控制工程",
 "status":"存疑——很可能已停招，勿据此备考",
 "evidence":[
  "南大电子科学与工程学院 2026 年复试笔试参考书目（官方 PDF）列出的 7 个专业中没有 085406",
  "唯一提及南大 085406 的是聚合站，标注为 2020 年、开设单位「工程管理学院」，该学院此后已重组",
  "南大 2026 年硕士招生目录页（yzb.nju.edu.cn/19/b1/c47862a793009/pagem.htm）正文为空，附件未渲染，无法核实",
 ],
 "howToVerify":"以研招网 yz.chsi.com.cn/zsml 按「南京大学 + 085406」查当年目录，或直接致电南大研招办",
 "note":"本库不为无法确认存在的专业建立记录——错误的专业课方向会直接浪费一整年复习"}
if not any(x.get("school")=="南京大学" and x.get("code")=="085406"
           for x in doc["completeness"]["verifyNeeded"]):
    doc["completeness"]["verifyNeeded"].append(item)

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
 "tuimianOnly":sum(1 for r in doc["records"] if r.get("tuimianOnly"))}
doc["completeness"]["sourceAccess"]["ok"].append(
 "南京理工大学：目录 PDF 在 gs.njust.edu.cn/_upload/ 下，含初试与复试科目")
doc["completeness"]["sourceAccess"]["blocked"].append(
 "南京大学：招生目录页正文为空、附件未渲染，只能靠各学院自己发的 PDF 补")
json.dump(doc, open(P,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"✓ 南理工 +{added} 条 → {dict(agg['南京理工大学'])}")
print(f"✓ 已登记存疑专业 {len(doc['completeness']['verifyNeeded'])} 条")
print("  全库:", doc["completeness"]["totals"])
