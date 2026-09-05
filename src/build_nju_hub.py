# -*- coding: utf-8 -*-
"""
生成南大 085406 控制工程专栏（data/nju.json 扩写）。

分层原则：
  official  —— 抓到学院/学校官网原文的
  secondary —— 第三方 App / 聚合站，未见官方原文
  unverified—— 单一来源且无佐证，只登记不当数据用
本专栏刻意把三者分开显示，因为这个专业本库此前判断出过错。
"""
import json, os
D = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
Q = os.path.join(D, "nju.json")
d = json.load(open(Q, encoding="utf-8"))

RA_HOME = "https://ra.nju.edu.cn/"
RA_INTRO= "https://ra.nju.edu.cn/xygk/xyjj/index.html"
YZB     = "https://yzb.nju.edu.cn/47862/listm.htm"
YZB_LINE= "https://yzb.nju.edu.cn/48336/listm.htm"
YZB_STAT= "https://yzb.nju.edu.cn/48337/listm.htm"
NJU_NEWS= "https://www.nju.edu.cn/info/1056/421891.htm"
TUIMIAN = "https://cacso.nju.edu.cn/09/85/c55718a788869/pagem.htm"

d["hub"] = {
 "title": "085406 控制工程（专硕）",
 "college": "机器人与自动化学院",
 "campus": "苏州校区",
 "addr": "江苏省苏州市太湖大道 1520 号",

 "official": {
  "label": "官方原文核实",
  "items": [
   {"k":"学院沿革","v":"前身为 2023 年成立的「南京大学前沿科学学院高端控制与智能运维研发中心」，2025 年经学校批准正式挂牌成立","src":RA_INTRO},
   {"k":"学科定位","v":"构建「机器人 + 自动化 + 人工智能」三位一体体系，主攻机器人系统工程、复杂系统的精密控制与运维、智能无人系统、控制理论与应用","src":RA_INTRO},
   {"k":"培养特色","v":"官方表述为「理论与实践并重、软件与硬件协同」，聚焦「智能控制」与「机器人技术」两大核心方向","src":RA_INTRO},
   {"k":"本科布局","v":"2025 年首开「自动化（机器人方向）」本科专业；2026 年 9 月本科教学实验室一期建成并迎首批本科生","src":RA_HOME},
   {"k":"学校层面确认","v":"南大官网新闻明确「在苏州校区新增自动化（机器人方向）招生专业」「新建机器人与自动化学院」","src":NJU_NEWS},
   {"k":"推免细则","v":"学院已发布 2026 年接收推荐免试研究生工作实施细则，说明研究生招生已在运行","src":TUIMIAN},
  ]},

 "secondary": {
  "label": "二手来源，报考前须以官方目录核对",
  "items": [
   {"k":"初试科目","v":"①101 思想政治理论 ②204 英语（二）③302 数学（二）④865 自动控制原理（经典 60%、现代 40%）"},
   {"k":"研究方向","v":"01 智能控制工程 / 02 机器人工程，两个方向初试科目相同"},
   {"k":"招生人数","v":"38 人。原页面注明「招生人数为专业招生总数，非方向人数」，且含推免，统考实际名额需减去推免"},
   {"k":"分数线","v":"320（2026 年展示值）；另有来源称该院执行校线 315"},
   {"k":"学位类型","v":"专硕 · 全日制 · 统考，有博士点"},
  ],
  "from":"掌上考研 App 专业页，页面注明数据引自南大研招网 yzb.nju.edu.cn",
  "src":YZB},

 "unverified": {
  "label": "单一来源、无官方佐证，仅登记不作数据用",
  "items": [
   "有聚合站称南大存在两个招生单位同招 085406：机器人与自动化学院与工程管理学院，"
   "后者 2025 复试线 360、拟招 27 人、复试考《微机原理与接口技术》、线下笔试加面试、不接受调剂与破格",
   "该站同时称两院均差额复试，工程管理学院复试比例不低于 120%，2024 年实际复录比 20 进 16",
   "上述内容出自单一聚合站且明显为 AI 生成（原文自述「根据知识库信息」），未获官方佐证",
  ],
  "why":"若属实，两个学院分数线差 40 分（320 对 360），报错院系代价极大，因此单列提醒而不并入数据",
 },

 "verifyPath": {
  "label": "自行核实的三个入口",
  "items": [
   {"k":"招生目录","v":"研招网「简章目录」栏，下载当年招生目录附件，按院系代码查机器人与自动化学院","url":YZB},
   {"k":"复试基本分数线","v":"研招网「复试基本分数线」栏，核对校线与院线","url":YZB_LINE},
   {"k":"往年报考录取统计","v":"研招网「往年报考录取统计」栏，这是判断真实难度最有用的一栏","url":YZB_STAT},
  ]},

 "notes": [
  "学院 2025 年才挂牌，2026 年才有首批本科生，研究生招生历史很短，历年分数线与报录比参考价值有限。",
  "本库此前曾据电科院一份文件误判该专业停招，已订正。判断停招需要招生目录级别的否定证据。",
  "865 自动控制原理与南京理工的 873、电子科大的 839、北信科的 803 均不同，专业课不可通用。",
 ],
}
d["updated"] = "2026-09"
json.dump(d, open(Q, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
h = d["hub"]
print("✓ nju.json hub 生成")
print(f"   official {len(h['official']['items'])} 条 · secondary {len(h['secondary']['items'])} 条 "
      f"· unverified {len(h['unverified']['items'])} 条 · 核实入口 {len(h['verifyPath']['items'])} 个")
