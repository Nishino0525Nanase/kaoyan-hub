# -*- coding: utf-8 -*-
"""
南京大学 085406 控制工程入库，并撤销此前「存疑停招」的错误判断。

订正说明：此前依据「电科院 2026 复试参考书目的 7 个专业中无 085406」推断该专业
已停招——这是把一个学院的清单当成了全校 0854 的全集。实际开设单位是
机器人与自动化学院（苏州校区，ra.nju.edu.cn），一个 2025 年才设、
2026 年 9 月迎首批本科生的新学院。

来源分级：
  学院存在性、办学校区 —— 学院官网，official
  初试科目/分数线/招生数 —— 掌上考研 App 截图（该 App 页面注明数据引自
      南大研招网 yzb.nju.edu.cn），属二手，标 secondary，待官方目录核实
  工程管理学院同招 085406 —— 聚合站单一来源，未核实，只登记不入记录
"""
import json, os
from collections import defaultdict
D = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
P = os.path.join(D, "programs.json")
doc = json.load(open(P, encoding="utf-8"))
proto = doc["records"][0]

RA   = "https://ra.nju.edu.cn/"
YZB  = "https://yzb.nju.edu.cn/47862/listm.htm"
def S(*p): return [{"code": c, "name": n} for c, n in p]
SUBJ = S(("101","思想政治理论"), ("204","英语（二）"), ("302","数学（二）"),
         ("865","自动控制原理（经典 60%、现代 40%）"))

added = 0
if not any(r["school"] == "南京大学" and r["code"] == "085406" for r in doc["records"]):
    rec = {k: ([] if isinstance(proto[k], list) else None) for k in proto}
    rec.update({
      "school":"南京大学","track":"ee","code":"085406","name":"控制工程",
      "college":"机器人与自动化学院","campus":"苏州校区","degree":"专硕",
      "dataYear":"2026","subjects":SUBJ,
      "directions":["01 智能控制工程","02 机器人工程"],
      "seats":{"plan":38,"note":"38 为专业招生总数，非单个方向人数；含推免，实际统考数需减去推免"},
      "lines":[{"year":2026,"score":320,"kind":"待核实","note":"来源为第三方 App 展示，未见官方原文"}],
      "sources":[{"url":RA,"official":True,"what":"学院存在性与办学校区"},
                 {"url":YZB,"official":True,"what":"南大研招网简章目录入口（该 App 注明数据引自此处）"}],
      "confidence":"secondary",
      "note":("开设单位为机器人与自动化学院（苏州校区），学院成立较新，2026 年 9 月迎首批本科生。"
              "初试科目、分数线 320、招生 38 人来自掌上考研 App 展示页（该页注明引自南大研招网），"
              "属二手来源，尚未在官方招生目录中核对原文——报考前务必以 yzb.nju.edu.cn 当年目录为准。"),
    })
    doc["records"].append(rec); added += 1

# 撤销错误的存疑登记，改为「已订正」+ 新的待核实项
vn = doc["completeness"].get("verifyNeeded", [])
vn = [x for x in vn if not (x.get("school")=="南京大学" and x.get("code")=="085406")]
vn.append({
 "school":"南京大学","code":"085406","name":"控制工程",
 "status":"已确认开设（此前本库误判为停招，已订正）",
 "evidence":[
  "开设单位为机器人与自动化学院（苏州校区），学院官网 ra.nju.edu.cn 可访问，2026 年 9 月迎首批本科生",
  "此前误判原因：把电子科学与工程学院的专业清单当成了全校 0854 的全集，未检索新设学院",
  "初试 101 + 204 英语二 + 302 数学二 + 865 自动控制原理（经典 60%、现代 40%），两个方向：01 智能控制工程、02 机器人工程",
 ],
 "stillUnverified":[
  "分数线 320 与招生 38 人：来自第三方 App 展示页，未见官方原文",
  "另有单一聚合站称工程管理学院同样招 085406（2025 复试线 360、拟招 27、复试考微机原理与接口技术），"
  "未获官方佐证，本库暂不建记录",
 ],
 "howToVerify":"以 yzb.nju.edu.cn 简章目录当年的招生目录附件为准，或致电机器人与自动化学院研究生教务",
})
doc["completeness"]["verifyNeeded"] = vn

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
json.dump(doc, open(P,"w",encoding="utf-8"), ensure_ascii=False, indent=1)

# 同步订正 nju.json
Q = os.path.join(D, "nju.json")
n = json.load(open(Q, encoding="utf-8"))
n["sources"].append({
 "what":"085406 控制工程的开设单位与办学校区","from":"南京大学机器人与自动化学院官网",
 "url":RA,"org":"机器人与自动化学院·苏州校区","type":"学院官网","year":"2026",
 "caveat":"学院官网未挂研究生招生专栏，科目与分数线需另找官方目录核实"})
n["sources"].append({
 "what":"085406 初试科目、分数线 320、招生 38 人、两个研究方向",
 "from":"掌上考研 App 专业页（页面注明数据引自南大研招网）","url":YZB,
 "org":"第三方 App","type":"二手展示页","year":"2026",
 "caveat":"未见官方原文，confidence=secondary，报考前必须以研招网当年目录核对"})
n["verifyNeeded"] = [x for x in vn if x.get("school")=="南京大学"]
n["correction"] = {
 "date":"2026-09",
 "what":"此前本库把南大 085406 判为「很可能已停招」，判断错误，现已订正",
 "why":"依据的是电子科学与工程学院 2026 复试参考书目的专业清单，把单个学院的清单当成了全校 0854 的全集；实际开设单位机器人与自动化学院是新设学院，未被检索到",
 "lesson":"一个学院的专业清单不能推断全校是否开设某专业；判断「停招」需要招生目录级别的否定证据，而不是某份文件里没提到"}
json.dump(n, open(Q,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"✓ programs +{added} 条；verifyNeeded {len(vn)} 条；nju.json 已加订正说明")
print("  全库:", doc["completeness"]["totals"])
