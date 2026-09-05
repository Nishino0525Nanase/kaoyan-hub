# -*- coding: utf-8 -*-
"""电子与通信工程学院(深圳)2025 复试细则入库。官网原文，全文可取。"""
import json, os
D = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
SRC = "https://sece.sysu.edu.cn/zs/zs01/1418328.htm"
P = os.path.join(D, "quota-retest.json")
doc = json.load(open(P, encoding="utf-8"))

RETEST = {
 "ratio": None,
 "weight": "复试成绩与初试成绩各占入学总成绩的 50%",
 "form": "现场复试，笔试 + 面试",
 "hasMachineTest": False,
 "subjects": ("专业课笔试占复试成绩 20%（科目同招生专业目录公布的复试专业课）"
              " + 外语应用能力测试 20%（面试）"
              " + 专业能力及综合素质考核 60%（面试）"),
 "duration": "每位考生复试总时间（含外语考核）不少于 20 分钟",
 "passLine": "复试成绩低于复试满分值的 60% 为不合格，不予录取",
 "tieBreak": "总成绩同分按初试排序；初试同分则以面试成绩（外语 + 专业能力及综合素质）排序",
 "note": "学硕与专硕分别排序、分别划定拟录取名单",
}
ROWS = [
 ("081000","信息与通信工程",57,35,22,325,45,45,65,65,None),
 ("085400","电子信息",       95,24,71,370,60,60,90,90,None),
 ("140100","集成电路科学与工程",1, 1, 0,325,45,45,65,65,"原文备注「无公开招考指标」"),
]
have = {(r["school"], r["code"], r.get("college")) for r in doc["records"]}
added = 0
for code,name,tot,tm,ex,ln,pol,en,c1,c2,extra in ROWS:
    key = ("中山大学", code, "电子与通信工程学院")
    if key in have: continue
    doc["records"].append({
      "school":"中山大学","track":"ee","code":code,"name":name,
      "college":"电子与通信工程学院","campus":"深圳校区",
      "quota":{"year":2025,"planTotal":tot,"tuimian":tm,"exam":ex,
               "tuimianRatio":round(tm/tot,3),
               "note":"细则原文三列：总计划／已招推免生／公开招考计划"
                      + ("；" + extra if extra else "")},
      "retest":dict(RETEST),
      "line":{"year":2025,"total":ln,"politics":pol,"english":en,
              "course1":c1,"course2":c2,"note":"院线，不分方向"},
      "sources":[{"url":SRC,"official":True}],"confidence":"official"})
    added += 1
doc["updated"] = "2026-09"
json.dump(doc, open(P,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"✓ quota-retest +{added} → 共 {len(doc['records'])} 条")
for r in doc["records"][-added:]:
    q=r["quota"]; l=r["line"]
    print(f"   {r['code']} {r['name'][:12]:<12} 线{l['total']} 单科{l['politics']}/{l['course1']}"
          f"  计划{q['planTotal']} 推免{q['tuimian']} 统考{q['exam']}")
