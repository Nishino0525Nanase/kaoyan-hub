# -*- coding: utf-8 -*-
"""南大机器人与自动化学院师资入库（官网专职教师页，official），并补南大资料链接。"""
import json, os
D = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
SRC = "https://ra.nju.edu.cn/szll/zzjs/index.html"
B = "http://ra.nju.edu.cn/szll/zzjs/"
P_, F_, Z_ = "教授", "副教授", "助理教授"

# (姓名, 职称, 研究方向, 页面id, 备注)
R = [
("周克敏",P_,"鲁棒控制，多目标优化控制，系统和控制器模型降阶，滞环非线性系统鲁棒控制，系统故障诊断与容错控制及其应用","20250901/i335910.html","学院院长"),
("周东华",P_,"动态系统故障诊断、运行安全性评估理论","20250901/i335912.html","学院名誉主任，兼职"),
("陈春林",P_,"强化学习、智能机器人、无人驾驶以及复杂系统建模、仿真与控制","20251120/i352846.html","学院副院长，IEEE Fellow"),
("李华雄",P_,"模式识别与智能系统、机器学习与数据挖掘、机器人多模态学习与控制、机器人视觉","20251121/i352917.html",None),
("鲁为民",P_,"自动控制、机器学习、强化学习、云计算、经典和生成式人工智能、产品管理、技术创新和产业化","20251204/i353737.html","顾问教授，兼职"),
("朱波",F_,"复杂无人系统建模与鲁棒协同控制","20250901/i335916.html","长聘副教授"),
("陈建琪",F_,"网络化系统控制、信息物理系统安全、鲁棒控制、机器学习与控制、机械臂协同等","20250901/i335914.html","准聘副教授"),
("杨博渊",F_,"工业装备智能运维，机器人多模态学习与控制","20250901/i335915.html","准聘副教授"),
("赵迪",F_,"鲁棒控制、安全控制、多模态学习、图像处理","20250901/i335913.html","准聘副教授"),
("许鑫",F_,"机器学习及其应用；局部与全局优化；物理信息神经网络在控制决策中的应用；高维模型表示理论及其在机器学习中的应用","20251119/i352813.html",None),
("王志",F_,"强化学习，具身智能","20251119/i352803.html","准聘副教授"),
("童鑫",F_,"混杂反馈控制、机器人规划与控制、多智能体协同控制、复杂网络生成","20250901/i335924.html","准聘副教授"),
("闫浩",F_,"机器人关节电机及其控制、电动飞行器推进技术、多端口电力电子变压器","20260403/i371555.html","准聘副教授，2026 年入职"),
("张建强",Z_,"半导体装备建模与超精密控制、光电跟踪控制、图像检测与目标识别","20250901/i335926.html",None),
("付瑞",Z_,"随机控制理论、随机热动力学、数学物理、最优化运输理论","20250901/i335925.html",None),
("周小彬",Z_,"空中机器人运动规划与控制系统设计","20250901/i335921.html",None),
("张君会",Z_,"信息物理安全、自主智能系统、可置信人工智能控制、机器人、自动驾驶","20250901/i335923.html",None),
("路洋",Z_,"信息物理系统的隐私与安全，多机器人系统的协同感知、决策与控制，联邦学习，安全强化学习","20250901/i335920.html",None),
("王丹",Z_,"复杂系统智能控制、鲁棒控制与相位理论、网络科学、多智能体系统协同控制、新能源电网","20250901/i335918.html",None),
("马英杰",Z_,"过程系统工程、数值优化、模型预测控制、机器学习、工业智能","20250901/i335919.html",None),
("魏婧雯",Z_,"机器学习、强化学习及其在储能系统健康评估、故障诊断与优化控制中的应用","20251125/i353102.html",None),
("孙宇祥",Z_,"具身智能、人机融合系统","20251119/i352800.html",None),
("梅文杰",Z_,"复杂系统的建模分析与控制（数据驱动方法、几何控制、系统安全性等）、人工智能、机器人技术等领域的交叉融合","20250901/i335917.html",None),
("吕尚可",Z_,"机器人运动控制、强化学习、具身智能","20251119/i352806.html",None),
("高岩",Z_,"无人机集群协同控制、多机器人系统安全控制、运动规划、抗扰控制","20260407/i372033.html",None),
]

# ---- 1. 导师名录：新增南大学院 ----
A = os.path.join(D, "advisors.json")
adv = json.load(open(A, encoding="utf-8"))
if not any(c["school"] == "南京大学" for c in adv["colleges"]):
    adv["colleges"].append({
      "id":"nju-ra","school":"南京大学","name":"机器人与自动化学院",
      "campus":"苏州校区","campusId":None,
      "site":"https://ra.nju.edu.cn/","source":SRC,"sourceLabel":"专职教师",
      "confidence":"official","fetched":"2026-09-01",
      "scope":"专职教师全部（教授、副教授、助理教授）；专职科研与博士后未收录",
      "advisors":[{"name":n,"title":t,"email":None,"areas":a,
                   "url":B+u,"note":nt,"advises":None,"directions":None}
                  for n,t,a,u,nt in R]})
for c in adv["colleges"]:
    c["count"] = len(c["advisors"])
adv["total"] = sum(c["count"] for c in adv["colleges"])
adv["schoolsCovered"] = len({c["school"] for c in adv["colleges"]})
done = {c["school"] for c in adv["colleges"]}
adv["gaps"] = sorted(n for n in adv["gaps"] if n not in done)
adv["coverage"]["covered"] = len(done)
adv["updated"] = "2026-09"
json.dump(adv, open(A,"w",encoding="utf-8"), ensure_ascii=False, indent=1)

# ---- 2. 南大专栏：加导师小结 ----
Q = os.path.join(D, "nju.json")
n = json.load(open(Q, encoding="utf-8"))
n["faculty"] = {"count":len(R),"source":SRC,"sourceLabel":"机器人与自动化学院 · 专职教师",
 "note":"官网专职教师页原文，含职称、研究方向与个人主页。专职科研与博士后未收录。",
 "byTitle":{"教授":sum(1 for x in R if x[1]==P_),"副教授":sum(1 for x in R if x[1]==F_),
            "助理教授":sum(1 for x in R if x[1]==Z_)},
 "highlights":[
  "周克敏（院长）：鲁棒控制、多目标优化控制、模型降阶、故障诊断与容错控制",
  "陈春林（副院长，IEEE Fellow）：强化学习、智能机器人、无人驾驶、复杂系统建模与控制",
  "闫浩：机器人关节电机及其控制、电动飞行器推进技术、多端口电力电子变压器——全院最偏硬件的一位",
  "张建强：半导体装备建模与超精密控制、光电跟踪控制",
 ],
 "read":"整体重心在控制理论、强化学习与具身智能，做电机/功率电子等纯硬件的很少，仅闫浩一人明显偏此方向。"}
n["sources"].append({"what":"学院 24 位专职教师的职称、研究方向与个人主页",
 "from":"机器人与自动化学院 · 专职教师","url":SRC,"org":"机器人与自动化学院·苏州校区",
 "type":"学院官网","year":"2026"})
n["updated"] = "2026-09"
json.dump(n, open(Q,"w",encoding="utf-8"), ensure_ascii=False, indent=1)

# ---- 3. 资料链接：新增南大分组 ----
Rf = os.path.join(D, "resources.json")
res = json.load(open(Rf, encoding="utf-8"))
G = {"title":"南京大学控制工程 · 官方信源",
 "desc":"085406 控制工程（机器人与自动化学院，苏州校区）。该专业本库曾误判停招，已订正，务必自行核对原文",
 "links":[
  {"name":"南京大学研究生招生网 · 简章目录","url":"https://yzb.nju.edu.cn/47862/listm.htm",
   "desc":"历年招生章程与招生目录。085406 的科目与招生数以这里的当年目录附件为准"},
  {"name":"研招网 · 复试基本分数线","url":"https://yzb.nju.edu.cn/48336/listm.htm",
   "desc":"核对校线与院线。有来源称该院执行校线，需自行确认"},
  {"name":"研招网 · 往年报考录取统计","url":"https://yzb.nju.edu.cn/48337/listm.htm",
   "desc":"报录比在这里，判断真实难度比看分数线有用得多"},
  {"name":"机器人与自动化学院官网","url":"https://ra.nju.edu.cn/",
   "desc":"2025 年 5 月挂牌的新学院，苏州校区太湖大道 1520 号"},
  {"name":"学院 · 专职教师","url":SRC,
   "desc":"24 位专职教师的职称、研究方向与个人主页，本库导师名录即出自此页"},
  {"name":"学院 · 学院简介","url":"https://ra.nju.edu.cn/xygk/xyjj/index.html",
   "desc":"官方学科定位：机器人系统工程、复杂系统精密控制与运维、智能无人系统、控制理论与应用"},
  {"name":"学院 · 通知公告","url":"http://ra.nju.edu.cn/xydt/tzgg/index.html",
   "desc":"推免细则、招生相关通知在这里发布"},
 ]}
res["groups"] = [g for g in res["groups"] if g["title"] != G["title"]]
i = next((k for k,g in enumerate(res["groups"]) if g["title"]=="中山大学官方信源"), 0)
res["groups"].insert(i+1, G)
res["updated"] = "2026-09"
json.dump(res, open(Rf,"w",encoding="utf-8"), ensure_ascii=False, indent=1)

print(f"✓ 导师 +{len(R)} 人 → 全库 {adv['total']} 人，覆盖 {adv['coverage']['covered']}/79 所")
print(f"✓ 南大专栏加师资小结；资料链接新增「{G['title']}」{len(G['links'])} 条")
