# -*- coding: utf-8 -*-
"""
中大系统科学与工程学院师资入库（官网教师队伍页，official）。

注意两点：
1) 该页把导师分三类：本院导师、联培导师、双聘导师。只收本院导师 27 人。
   联培导师（院士 3 + 博导 66 + 硕导 26）多为校外单位人员，双聘导师
   本职在数学/电信/电通/计算机等其他学院，都已在各自学院统计过，
   混进来会重复计数、也会让人误以为该院自有师资规模很大。
2) 该页只给姓名与个人主页，不含研究方向与邮箱，areas 一律留空。
3) 官网页脚办公地址为「广州市海珠区新港西路135号」，
   与本库此前按公开院系设置归入珠海校区不符，一并订正为广州·南校园。
"""
import json, os
D = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
SRC = "https://ssse.sysu.edu.cn/teachers"
B = "https://ssse.sysu.edu.cn/teacher/"
P_, F_, Z_ = "教授", "副教授", "助理教授"

R = [
 ("伍蔡伦",P_,"1240"),("庄学彬",P_,"91"),("陈洪波",P_,"75"),("李雄",P_,"667"),
 ("肖绍球",P_,"1014"),("张涛",P_,"241"),("易卿武",P_,"1523"),("修保新",P_,"236"),
 ("黄寒砚",P_,"138"),
 ("王劲博",F_,"89"),("冯展祥",F_,"1075"),("朱永利",F_,"897"),("伍朝显",F_,"735"),
 ("孙蕾",F_,"88"),("许丹",F_,"1275"),("李灏峰",F_,"1382"),("吴贺丰",F_,"1282"),
 ("杨凌霄",F_,"1236"),("张传富",F_,"311"),("张岐良",F_,"203"),("罗宗富",F_,"280"),
 ("段焰辉",F_,"86"),("钟令枢",F_,"1015"),("侯燕青",F_,"252"),("侯治威",F_,"205"),
 ("戚煜华",F_,"1016"),
 ("刘熙",Z_,"697"),
]

A = os.path.join(D, "advisors.json")
adv = json.load(open(A, encoding="utf-8"))
NAME = "系统科学与工程学院"
adv["colleges"] = [c for c in adv["colleges"] if c["name"] != NAME]
adv["colleges"].append({
  "id":"sysu-ssse","school":"中山大学","name":NAME,"campus":"广州·南校园","campusId":None,
  "site":"https://ssse.sysu.edu.cn/","source":SRC,"sourceLabel":"教师队伍",
  "confidence":"official","fetched":"2026-09-01",
  "scope":("仅本院导师 27 人。该页另列联培导师（院士 3、博导 66、硕导 26，多为校外单位）"
           "与双聘导师（本职在数学/电信/电通/计算机等学院，已在各自学院统计），均未收录以免重复计数。"
           "该页不含研究方向与邮箱"),
  "advisors":[{"name":n,"title":t,"email":None,"areas":None,"url":B+i,
               "note":None,"advises":None,"directions":None} for n,t,i in R]})
for c in adv["colleges"]:
    c["count"] = len(c["advisors"])
adv["total"] = sum(c["count"] for c in adv["colleges"])
adv["schoolsCovered"] = len({c["school"] for c in adv["colleges"]})
adv["updated"] = "2026-09"
json.dump(adv, open(A,"w",encoding="utf-8"), ensure_ascii=False, indent=1)

# 校区订正
S = os.path.join(D, "sysu.json"); d = json.load(open(S, encoding="utf-8"))
by={c['name']:c['count'] for c in adv['colleges'] if c['school']=='中山大学'}
SITE={c['name']:c.get('site') for c in adv['colleges'] if c['school']=='中山大学'}
for key in ('compare884','compare085403','compare085400'):
    for r in d[key]['rows']: r['advisors']=by.get(r['college'])
# 把系统院从珠海挪到广州
moved=None
for c in d['campuses']:
    for x in list(c['colleges']):
        if x['name']==NAME:
            moved=x; c['colleges'].remove(x)
if moved:
    gz=next((c for c in d['campuses'] if c['name']=='广州·东校园'), None)
    d['campuses'].append({"name":"广州·南校园","dorm":None,"colleges":[moved]})
for c in d['campuses']:
    for x in c['colleges']:
        x['advisors']=by.get(x['name'])
        if SITE.get(x['name']): x['site']=SITE[x['name']]
d['campuses']=[c for c in d['campuses'] if c['colleges']]
d['campusNote']=("只统计专硕记录。校区归属以学院官网标注的办公地址为准："
 "系统科学与工程学院官网页脚为广州市海珠区新港西路135号，故列在广州·南校园，"
 "此前按公开院系设置误归珠海，已订正。其余未逐一核实的仍按公开院系设置归组。"
 "「导师数」空白表示该学院师资尚未采集。")
d['index']['advisors']=sum(by.values()); d['index']['advisorColleges']=list(by)
d['sources']['items'].append({
 "what":"系统科学与工程学院 27 位本院导师名单与个人主页",
 "from":"系统科学与工程学院 · 教师队伍","url":SRC,
 "org":"系统科学与工程学院·广州南校园","type":"学院官网","year":"2026",
 "caveat":"该页只给姓名与主页链接，无研究方向与邮箱；联培与双聘导师未收录以免重复计数"})
d['updated']='2026-09'
json.dump(d, open(S,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"✓ 系统院 {len(R)} 人（教授 9、副教授 17、助理教授 1）")
print(f"  全库 {adv['total']} 人 / {len(adv['colleges'])} 个学院")
print("  校区分组:", [(c['name'], len(c['colleges'])) for c in d['campuses']])
