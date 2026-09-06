# -*- coding: utf-8 -*-
"""中大海洋工程与技术学院（珠海，085400 拟招 27）师资入库。官网全体教师页，official。"""
import json, os
D = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
SRC = "https://soet.sysu.edu.cn/zh-hans/faculty"
B = "https://soet.sysu.edu.cn/zh-hans/teacher/"
M = "@mail.sysu.edu.cn"
P_, F_, Z_, J_ = "教授", "副教授", "助理教授", "讲师"

# (姓名, 职称, 邮箱前缀, 研究方向, id, 备注)
R = [
("蔡华阳",P_,"caihy7","海洋环境监测与大数据应用","102",None),
("邓锐",P_,"dengr23","船海流固耦合与资源开发技术","170",None),
("郭志群",P_,"guozhq5","水下智能控制与无人观测技术","172",None),
("黄硕",P_,"huangsh97","船海流固耦合与资源开发技术","174",None),
("胡青",P_,"huqing3","水声信息感知与目标探测技术","94",None),
("贾良文",P_,"jialw","海洋环境监测与大数据应用","99",None),
("李整林",P_,"lizhlin29","水声信息感知与目标探测技术","700",None),
("苗建明",P_,"miaojm","水声信息感知与目标探测技术","298",None),
("马勇",P_,"mayong3","船海流固耦合与资源开发技术","35",None),
("孙鹏楠",P_,"sunpn","船海流固耦合与资源开发技术","133",None),
("文洪涛",P_,"wenht6","水声信息感知与目标探测技术","1246",None),
("王凯",P_,"wangkai25","船海流固耦合与资源开发技术","333",None),
("徐灵基",P_,"xulj26","水声信息感知与目标探测技术","336",None),
("许亮斌",P_,"xulb3","船海流固耦合与资源开发技术","650","学科带头人"),
("谢鹏",P_,"xiep9","海洋工程结构安全与监测技术","78","国家重点研发计划首席科学家"),
("杨清书",P_,"yangqsh","海洋动力过程与海岸工程","89",None),
("张铁栋",P_,"zhangtd5","水下智能控制与无人观测技术；海洋机器人技术、水下环境感知、水下航行器控制、新概念海洋无人系统","651","招生专业含自动控制、计算机、机器人"),
("陈顺华",F_,"chenshh73","海洋工程结构安全与监测技术","136",None),
("杜现平",F_,"duxp3","海洋工程结构安全与监测技术","171",None),
("冯帆",F_,"fengf35","新能源（储能）电力变换；水下无线充电；智能微网建模与控制","343",None),
("侯正瑜",F_,"houzhy7","水声信息感知与目标探测技术","730",None),
("姜大鹏",F_,"jiangdp5","水下智能控制与无人观测技术","176",None),
("蒋运华",F_,"jiangyh35","水下智能控制与无人观测技术","178",None),
("刘念念",F_,"liunn23","船海流固耦合与资源开发技术","181",None),
("刘一宁",F_,"liuyn223","水声信息感知与目标探测技术","1135",None),
("李倩倩",F_,"liqq","水声信息感知与目标探测技术","1180",None),
("刘涛",F_,"liutao55","水声信息感知与目标探测技术","352","招生专业含电子信息"),
("李晓天",F_,"lixiaot5","海洋工程结构安全与监测技术","179",None),
("刘锋",F_,"liuf53","海洋环境监测与大数据应用","180",None),
("倪问池",F_,"niwch","船海流固耦合与资源开发技术","313",None),
("牛丽霞",F_,"niulixia","海洋环境监测与大数据应用","315",None),
("彭超",F_,"pengch85","水下智能控制与无人观测技术","318",None),
("彭玉祥",F_,"pengyx55","船海流固耦合与资源开发技术","323",None),
("钱国伟",F_,"qiangw3","海洋工程结构与安全监测技术","673",None),
("任磊",F_,"renlei7","水声信息感知与目标探测技术；人工智能海洋学、海洋多尺度动力过程、海洋数值模拟与资料同化","325","招生专业含电子信息"),
("苏焱",F_,"suyan23","船海流固耦合与资源开发技术","327",None),
("吴铁成",F_,"wutch7","船海流固耦合与资源开发技术","370",None),
("吴晓笛",F_,"wuxd23","水声信息感知与目标探测技术","353",None),
("王立国",F_,"wanglg7","水下智能控制与无人观测技术","328",None),
("魏稳",F_,"weiw95","河口沉积动力学，海岸生物地貌，生态海堤工程","334",None),
("肖鹏",F_,"xiaop36","水声信息感知与目标探测技术","335",None),
("杨健敏",F_,"yangjm33","水声信息感知与目标探测技术；水声通信组网与跨介质信息高效传输","339",None),
("赵波",F_,"zhaob59","水声信息感知与目标探测技术","649",None),
("张淏酥",F_,"zhanghs7","水下智能控制与无人观测技术","340",None),
("查若思",F_,"zhars","水声信息感知与目标探测技术","355",None),
("张晓鹤",F_,"zhangxh258","海洋动力过程与海岸工程","750",None),
("张旭",F_,"zhangx798","船海流固耦合与资源开发技术","358",None),
("陈嘉豪",Z_,"chenjh598","船海流固耦合与资源开发技术","870",None),
("欧素英",J_,"ousuying","海洋动力过程与海岸工程","361",None),
]

A = os.path.join(D, "advisors.json")
adv = json.load(open(A, encoding="utf-8"))
NAME = "海洋工程与技术学院"
adv["colleges"] = [c for c in adv["colleges"] if c["name"] != NAME]
adv["colleges"].append({
  "id":"sysu-soet","school":"中山大学","name":NAME,"campus":"珠海校区","campusId":"zhuhai",
  "site":"https://soet.sysu.edu.cn/zh-hans","source":SRC,"sourceLabel":"全体教师",
  "confidence":"official","fetched":"2026-09-01",
  "scope":"教研岗教师（教授、副教授、助理教授、讲师）；博士后与专职科研人员未收录",
  "advisors":[{"name":n,"title":t,"email":(e+M if e else None),"areas":a,
               "url":B+i,"note":nt,"advises":None,"directions":None}
              for n,t,e,a,i,nt in R]})
for c in adv["colleges"]:
    c["count"] = len(c["advisors"])
adv["total"] = sum(c["count"] for c in adv["colleges"])
adv["schoolsCovered"] = len({c["school"] for c in adv["colleges"]})
adv["updated"] = "2026-09"
json.dump(adv, open(A,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
from collections import Counter
c = Counter(x[1] for x in R)
print(f"✓ 海工院 {len(R)} 人：" + "、".join(f"{k} {v}" for k,v in c.items()))
print(f"  全库 {adv['total']} 人 / {len(adv['colleges'])} 个学院")
