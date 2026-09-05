# -*- coding: utf-8 -*-
"""
生成 data/sysu.json —— 中山大学专栏的数据源。

定位：本库其余部分是横向比 147 所学校；这个专栏是纵向把一所学校挖透。
内容分两类：
  A. 聚合已有数据（导师/宿舍/专业/复试细则分散在四个文件里，这里给出索引）
  B. 本轮新采的校级信息：调剂政策、时间线、按校区的横向对比

所有条目均标 source 与 official，二手转述不收。
"""
import json, os
D = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
def rd(f): return json.load(open(os.path.join(D, f), encoding="utf-8"))

prog, adv, dorm, quota = rd("programs.json"), rd("advisors.json"), rd("dorms.json"), rd("quota-retest.json")
SR = [r for r in prog["records"] if r["school"] == "中山大学"]

SSSE = "https://ssse.sysu.edu.cn/article/1295"
GRAD = "https://graduate.sysu.edu.cn/zsw/"

doc = {
 "school": "中山大学",
 "updated": "2026-09",
 "note": ("中山大学专栏：把散在导师名录、校区住宿、专业方向、复试细则里的中大数据"
          "聚到一处，并补充校级政策。全部来自学校或学院官网，二手转述不收录。"),

 # ── 校区 × 学院 全景 ──────────────────────────────────
 "campuses": [
  {"id":"guangzhou-east","name":"广州·东校园","addr":"广州市番禺区大学城外环东路 132 号",
   "colleges":[{"name":"电子与信息工程学院（微电子学院）","site":"https://seit.sysu.edu.cn/",
                "advisors":85,"retestRule":"https://seit.sysu.edu.cn/article/2746"}],
   "dormRooms":33,"dormFee":"1500–5700 元/学年"},
  {"id":"shenzhen","name":"深圳校区","addr":"深圳市光明区公常路 66 号",
   "colleges":[{"name":"集成电路学院","site":"https://sic.sysu.edu.cn/",
                "advisors":27,"retestRule":"https://sic.sysu.edu.cn/rc/rc05/1418351.htm"},
               {"name":"电子与通信工程学院","site":"https://sece.sysu.edu.cn/",
                "advisors":58,"retestRule":"https://sece.sysu.edu.cn/zs/zs01/1418328.htm"}],
   "dormRooms":6,"dormFee":"1300–5200 元/学年"},
  {"id":"zhuhai","name":"珠海校区","addr":"珠海市香洲区唐家湾镇大学路 2 号",
   "colleges":[{"name":"微电子科学与技术学院","site":"https://mst.sysu.edu.cn/",
                "advisors":32,"retestRule":"https://mst.sysu.edu.cn/article/1191"}],
   "dormRooms":24,"dormFee":"1600–5200 元/学年"},
 ],

 # ── 085403 三校区横向对比（本库最核心的一张表）──────────
 "compare085403": {
  "title": "085403 集成电路工程 · 三校区对比",
  "sameInitial": "三个学院初试完全相同：101 思想政治理论 + 204 英语二 + 302 数学二 + 885 电子技术（数字和模拟）",
  "rows": [
   {"campus":"广州·东校园","college":"电子与信息工程学院（微电子学院）",
    "plan2026":81,"plan2025":82,"tuimian2025":28,"exam2025":54,"line2025":340,
    "retestForm":"笔试 + 面试","retestSubject":"专业课笔试考复试专业课；复试总分 500，占 50%",
    "advisors":85},
   {"campus":"珠海校区","college":"微电子科学与技术学院",
    "plan2026":34,"plan2025":34,"tuimian2025":23,"exam2025":11,"line2025":336,
    "retestForm":"纯面试，无笔试","retestSubject":"综合评价 20% + 外语 20% + 专业能力及综合素质 60%",
    "advisors":32},
   {"campus":"深圳校区","college":"集成电路学院",
    "plan2026":20,"plan2025":None,"tuimian2025":None,"exam2025":None,"line2025":None,
    "retestForm":"笔试 + 面试","retestSubject":"专业课笔试 100 分：模拟电路 + 数字电路 + 半导体物理，闭卷 2 小时",
    "advisors":27},
  ],
  "caveat": ("深圳集成电路学院 2025 细则中的分数线表与招生人数表是图片、无文字层，取不到，"
             "故留空——是还没查到，不是不招。三校区 2025 数据口径一致时才可直接比。"),
 },

 # ── 调剂政策（本轮新采，很多人忽略）────────────────────
 "transfer": {
  "keyFact": "中大因第一志愿生源充足，不接收校外调剂——没进复试只能校内调剂或调出中大",
  "source": SSSE, "official": True, "year": 2025,
  "example": {
    "college": "系统科学与工程学院",
    "accepts": [
     {"code":"085400","name":"电子信息","plan":11,"retestSlots":22,
      "line":"总分 300 / 政治 50 / 外语 50 / 业务课 60·60",
      "from":"优先接收第一志愿报考中大电信院、电通院、计算机学院的 085400、085404、081200 未被录取者"},
     {"code":"081000","name":"信息与通信工程","plan":2,"retestSlots":4,
      "line":"总分 280 / 政治 45 / 外语 45 / 业务课 60·60",
      "from":"只面向第一志愿报考中大 081000、081200 未被录取者"},
    ],
    "require": "统考科目相同；自命题科目相同或相近",
    "window": "2025 年为 3 月 28 日发布至 3 月 31 日 24:00 截止，窗口只有 3 天",
  },
 },

 # ── 时间线 ────────────────────────────────────────
 "timeline": [
  {"when":"2026 年 9 月","what":"2027 级招生简章与专业目录预计发布","note":"只认研招网，发布后核对统考名额、专业课代码、外语科目是否变动","src":GRAD},
  {"when":"2026-10-10 ~ 10-13","what":"预报名","note":"每日 9:00–22:00"},
  {"when":"2026-10-16 ~ 10-27","what":"正式网上报名","note":"每日 9:00–22:00"},
  {"when":"2026-12-10 ~ 12-21","what":"准考证打印"},
  {"when":"2026-12-20 ~ 12-21","what":"初试"},
  {"when":"2027 年 3 月中","what":"校线公布、各学院陆续发复试细则","note":"院线普遍高于校线，以报考学院公布的为准"},
  {"when":"2027 年 3 月下旬","what":"校内调剂窗口","note":"窗口通常只有 3–4 天，且中大不接收校外调剂"},
 ],

 # ── 报考要点（均可回溯到官方原文）──────────────────────
 "keyPoints": [
  {"t":"初试复试各占 50%","d":"电信院、微电子学院、集成电路学院的细则口径一致，复试权重很高","src":"https://seit.sysu.edu.cn/article/2746"},
  {"t":"复试低于满分 60% 直接不合格","d":"复试满分 500 的学院即低于 300 分不予录取，与总成绩排名无关","src":"https://sic.sysu.edu.cn/rc/rc05/1418351.htm"},
  {"t":"招生计划数不等于统考名额","d":"微电子学院 085403 总计划 34，但已招推免 23，公开招考仅 11","src":"https://mst.sysu.edu.cn/article/1191"},
  {"t":"院线普遍高于校线","d":"2025 年微电子学院 085403 院线 336、电信院 340，都高于校线","src":GRAD},
  {"t":"140100 集成电路科学与工程仅招推免","d":"集成电路学院、微电子学院、电通院三处均为仅推免，统考生报不了；走统考只能报 085403 专硕"},
  {"t":"不接收校外调剂","d":"第一志愿生源充足，校外调剂不接收，校内调剂窗口也很短","src":SSSE},
 ],

 # ── 数据索引：本库中大数据分布 ──────────────────────
 "index": {
  "programs": len(SR),
  "programsWithSubjects": sum(1 for r in SR if r.get("subjects")),
  "advisors": sum(c["count"] for c in adv["colleges"] if c["school"] == "中山大学"),
  "advisorColleges": [c["name"] for c in adv["colleges"] if c["school"] == "中山大学"],
  "dormRooms": next((s["count"] for s in dorm["schools"] if s["school"] == "中山大学"), 0),
  "retestRules": sum(1 for r in quota["records"] if r["school"] == "中山大学"),
 },
}
json.dump(doc, open(os.path.join(D, "sysu.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("✓ sysu.json 生成")
print("  索引:", json.dumps(doc["index"], ensure_ascii=False))
print("  校区:", [c["name"] for c in doc["campuses"]])
print("  要点:", len(doc["keyPoints"]), "条 | 时间线:", len(doc["timeline"]), "条")
