# -*- coding: utf-8 -*-
"""
中大珠海(微电子科学与技术学院)与深圳(集成电路学院)2025 复试细则入库。
两份均为学院官网原文。注意差异：珠海是纯面试，深圳有闭卷专业课笔试。
深圳那份的分数线与招生人数在原文中是图片，取不到，相应字段留空。
"""
import json, os
D = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
P = os.path.join(D, "quota-retest.json")
doc = json.load(open(P, encoding="utf-8"))

MST = "https://mst.sysu.edu.cn/article/1191"
SIC = "https://sic.sysu.edu.cn/rc/rc05/1418351.htm"

NEW = [
 {"school":"中山大学","track":"ee","code":"085403","name":"集成电路工程",
  "college":"微电子科学与技术学院","campus":"珠海校区",
  "quota":{"year":2025,"planTotal":34,"tuimian":23,"exam":11,"tuimianRatio":0.676,
           "note":"细则原文三列：总计划34／已招推免23／公开招考11。推免占比接近七成"},
  "retest":{"ratio":None,
    "weight":"复试成绩与初试成绩各占入学总成绩的 50%",
    "form":"现场复试，采取面试方式，无笔试",
    "hasMachineTest":False,
    "subjects":"综合评价 20% + 外语应用能力测试 20% + 专业能力及综合素质考核 60%",
    "duration":"每位考生复试总时间（含外语考核）不少于 20 分钟",
    "passLine":"复试成绩低于复试满分值的 60% 为不合格，不予录取",
    "tieBreak":"总成绩同分按初试成绩排序；初试再同分则以初试「业务课二」排序"},
  "line":{"year":2025,"total":336,"politics":50,"english":50,"course1":60,"course2":60,
          "note":"院线，不分方向。同院 080900 电子科学与技术(02 电路与系统)为 280/45/45/60/60"},
  "sources":[{"url":MST,"official":True}],"confidence":"official"},

 {"school":"中山大学","track":"ee","code":"085403","name":"集成电路工程",
  "college":"集成电路学院","campus":"深圳校区",
  "quota":{"year":2025,"planTotal":None,"tuimian":None,"exam":None,"tuimianRatio":None,
           "note":"细则原文中的招生人数表是图片，无文字层，取不到——空缺是还没查到，不是不招"},
  "retest":{"ratio":None,
    "weight":"复试总分 500 分，占入学总成绩的 50%",
    "form":"现场复试，笔试 + 面试",
    "hasMachineTest":False,
    "subjects":("专业课笔试 100 分：专业基础综合（模拟电路、数字电路、半导体物理），闭卷，2 小时"
                " + 外语应用能力测试 100 分（面试）"
                " + 专业能力及综合素质考核 300 分（面试）"),
    "duration":"面试总时间（含外语考核）不少于 20 分钟",
    "passLine":"复试成绩低于满分 60%（即 300 分）为不合格，不予录取",
    "tieBreak":"总成绩同分按初试排序；初试同分按复试排序；复试仍同分则以专业课笔试排序"},
  "line":{"year":2025,"total":None,"politics":None,"english":None,
          "course1":None,"course2":None,
          "note":"细则原文的分数线表为图片，取不到"},
  "sources":[{"url":SIC,"official":True}],"confidence":"official"},
]

have = {(r["school"], r["code"], r.get("college")) for r in doc["records"]}
added = 0
for r in NEW:
    if (r["school"], r["code"], r["college"]) in have:
        continue
    doc["records"].append(r); added += 1
doc["updated"] = "2026-09"
doc["why"] = doc.get("why") or ""
json.dump(doc, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"✓ quota-retest +{added} 条，共 {len(doc['records'])} 条")
for r in doc["records"][-added:]:
    q = r["quota"]
    print(f"   {r['campus']:<8}{r['college']:<18} 线{r['line']['total']} "
          f"计划{q['planTotal']} 推免{q['tuimian']} 统考{q['exam']}  {r['retest']['form']}")
