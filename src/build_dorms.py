# -*- coding: utf-8 -*-
"""
生成 data/dorms.json。
数据逐行抄自《2025学年中山大学学生宿舍住宿费收费标准公示表》（学校信息公开网 PDF）。
只收录国内生房型，国际生房型（价格是另一套体系）不收录。
注意：该表只公示「楼栋 → 房型/面积/价格/设备」，
      不公示「哪栋楼分给研究生、哪栋分给本科生」——所以本文件里没有这个字段，也不推测。
"""
import json, os

SRC = ("https://xxgk.sysu.edu.cn/sites/default/files/2025-07/"
       "2025%E5%AD%A6%E5%B9%B4%E4%B8%AD%E5%B1%B1%E5%A4%A7%E5%AD%A6%E5%AD%A6%E7%94%9F"
       "%E5%AE%BF%E8%88%8D%E4%BD%8F%E5%AE%BF%E8%B4%B9%E6%94%B6%E8%B4%B9%E6%A0%87%E5%87%86"
       "%E5%85%AC%E7%A4%BA%E8%A1%A8.pdf")

# 设备条件在表里重复度极高，抽成常量避免文件膨胀
F_STD = "有电梯，床架、书桌、储物柜、风扇、网络端口，阳台，独立卫生间，室内有供热水、冷气设备"
F_GZ  = "有电梯、床、桌椅、书架、储物柜、阳台、风扇、光纤网络端口，独立卫生间，室内有供热水、冷气设备"
F_SZ  = "有电梯、独立卫生间、阳台，有床架、书桌、储物柜，室内有供热水、冷气设备"
F_ZH  = "有电梯、独立卫生间、阳台，有床架、书桌、储物柜，室内有供热水、冷气设备"
F_LY3 = "有电梯、写字台、单人床、单人衣柜、坐椅、网线接口、独立卫生间，室内有供热水、冷气设备"

# (楼栋, 等级, 床位数, 人均建筑面积㎡, 住宿费元/学年, 设备)
EAST = [
 ("格致园3号-1单元（原东苑宾馆博士生宿舍）","引资新建",1,"35",4500,F_GZ),
 ("格致园3号-1单元（原东苑宾馆博士生宿舍）","引资新建",2,"22",3000,F_GZ),
 ("格致园3号-1单元7楼","引资新建",1,"31.2",4500,F_GZ),
 ("格致园3号-2单元","引资新建",4,"7.5",1500,F_GZ),
 ("格致园3号-3单元2楼","引资新建",1,"32",4600,F_GZ),
 ("格致园3号-3单元","引资新建",1,"44",5700,F_STD),
 ("格致园3号-3单元","引资新建",2,"22",3100,F_STD),
 ("格致园3号-4单元","引资新建",4,"8",1600,F_STD),
 ("明德园一号","引资新建",4,"11",1600,F_STD),
 ("明德园二号","引资新建",4,"11",1600,F_STD),
 ("明德园三号","引资新建",4,"11",1600,F_STD),
 ("明德园五号","引资新建",4,"11",1600,F_STD),
 ("明德园七号","引资新建",4,"11",1600,F_STD),
 ("明德园八号","引资新建",4,"11",1600,F_STD),
 ("明德园九号","引资新建",4,"11",1600,F_STD),
 ("明德园十号","引资新建",4,"11",1600,F_STD),
 ("明德园十二号","引资新建",4,"11",1600,F_STD),
 ("慎思园五号","引资新建",4,"11",1600,F_STD),
 ("慎思园六号","引资新建",4,"11",1600,F_STD),
 ("慎思园七号","引资新建",4,"11",1600,F_STD),
 ("慎思园八号","引资新建",4,"11",1600,F_STD),
 ("慎思园九号","引资新建",4,"11",1600,F_STD),
 ("慎思园十号","引资新建",4,"11",1600,F_STD),
 ("至善园一号","引资新建",4,"11",1600,F_STD),
 ("至善园二号","引资新建",4,"11",1600,F_STD),
 ("至善园三号","引资新建",4,"11",1600,F_STD),
 ("至善园四号","引资新建",4,"11",1600,F_STD),
 ("至善园五号","引资新建",4,"11",1600,F_STD),
 ("至善园六号","引资新建",4,"11",1600,F_STD),
 ("至善园七号","引资新建",4,"11",1600,F_STD),
 ("至善园八号","引资新建",4,"11",1600,F_STD),
 ("至善园九号","引资新建",4,"11",1600,F_STD),
 ("至善园十号","引资新建",4,"11",1600,F_STD),
]

SZ = [
 ("西区学生宿舍","一级",4,"13",1300,F_SZ),
 ("西区学生宿舍","一级",2,"19",2600,F_SZ),
 ("西区学生宿舍","一级",1,"37",5200,F_SZ),
 ("东区学生宿舍","一级",4,"12.49-12.55",1300,F_SZ),
 ("东区学生宿舍","一级",2,"18.42-18.8",2600,F_SZ),
 ("东区学生宿舍","一级",1,"37",5200,F_SZ),
]

ZH = [
 ("荔园3号","一级",2,"15.5",2500,F_LY3),
 ("荔园3号","一级",1,"31",4900,F_LY3),
 ("荔园5号","引资新建",4,"9",1600,F_STD),
 ("荔园7号","引资新建",4,"9",1600,F_STD),
 ("荔园8号","引资新建",4,"10",1600,F_STD),
 ("荔园9号","引资新建",4,"9",1600,F_STD),
 ("荔园11号","引资新建",4,"9",1600,F_STD),
 ("荔园15号","引资新建",3,"14",1900,F_STD),
 ("荔园16号","引资新建",3,"14",1900,F_STD),
 ("荔园17号","引资新建",4,"10",1600,F_STD),
 ("荔园18号","引资新建",4,"10",1600,F_STD),
 ("荔园19号","引资新建",4,"10",1600,F_STD),
 ("榕园5号","引资新建",4,"10",1600,F_STD),
 ("榕园6号","引资新建",4,"11",1600,F_STD),
 ("榕园7号","引资新建",4,"11",1600,F_STD),
 ("榕园8号","引资新建",4,"11",1600,F_STD),
 ("榕园9号","引资新建",4,"11",1600,F_STD),
 ("榕园10号","引资新建",4,"8",1600,F_STD),
 ("榕园11号","引资新建",4,"11",1600,F_STD),
 ("榕园12号","引资新建",4,"11",1600,F_STD),
 ("北区研究生宿舍（槿园）","一级",1,"38.95",5200,F_ZH),
 ("北区研究生宿舍（槿园）","一级",2,"19.49",2600,F_ZH),
 ("荔园研究生宿舍（桐园）","一级",1,"29.61",5200,F_ZH),
 ("荔园研究生宿舍（桐园）","一级",2,"14.8",2600,F_ZH),
]

def rooms(rows):
    return [{"building":b,"tier":t,"beds":n,"area":a,"fee":f,"facilities":fac}
            for b,t,n,a,f,fac in rows]

def stats(rows):
    fees = [r[4] for r in rows]
    beds = sorted({r[2] for r in rows})
    return {"min": min(fees), "max": max(fees), "bedTypes": beds}

# ── 华中科技大学 · 主校区 / 同济校区 ────────────────────────────
# 来源《华中科技大学2024年研究生新生入学须知》(研招网转载)
# 这份比中大那张表更对口——它本身就是研究生口径。
F_HUST4 = "四人间"
HUST_MAIN = [
 ("韵苑一/二/四栋，东六/七舍，西一/二/五/六/八/九/十四/十五舍","—",4,None,1120,"四人间"),
 ("东九/十/十二舍，南一/二/三舍","—",4,None,1320,"四人间"),
 ("东一舍，教七/八舍，西四/七/十/十一/十二/十三/十六/十七舍","—",2,None,1440,"双人间"),
 ("博士生公寓1-4栋","—",2,None,1740,"双人间（博士生公寓）"),
 ("博士生公寓1-4栋","—",1,None,2080,"单人间（博士生公寓）"),
 ("博士生公寓1-4栋","—",1,None,2480,"无障碍间（博士生公寓）"),
 ("新博士生公寓A、B栋","—",1,None,1980,"套房内单人间（博士生公寓）"),
]
HUST_TJ = [
 ("学子苑502栋（博士生宿舍）","—",2,None,1440,"双人间"),
 ("学子苑505栋、506栋","—",4,None,1320,"四人间"),
]

def rooms2(rows):
    return [{"building":b,"tier":(t if t!="—" else None),"beds":n,"area":a,
             "fee":f,"facilities":fac} for b,t,n,a,f,fac in rows]

def stats2(rows):
    fees=[r[4] for r in rows]; beds=sorted({r[2] for r in rows})
    return {"min":min(fees),"max":max(fees),"bedTypes":beds}

SYSU = {
 "school":"中山大学","granularity":"building",
 "audience":"公示表未区分本科生 / 研究生，只按楼栋公示",
 "confidence":"official","dataYear":"2025学年",
 "source":SRC,"sourceLabel":"2025学年中山大学学生宿舍住宿费收费标准公示表",
 "sourcePage":"https://xxgk.sysu.edu.cn/cat/122","fetched":"2026-09-01",
 "scope":("已录入东校园、深圳校区、珠海校区的全部国内生房型（对应导师名录里四个学院所在校区）。"
          "南校园、北校园房型数量庞大（原表 18 页），尚未逐行录入。国际生房型不收录。"),
 "campuses":[
   {"id":"east","name":"东校园","city":"广州市番禺区大学城外环东路 132 号",
    "colleges":["电子与信息工程学院（微电子学院）"],
    "rooms":rooms(EAST),"stats":stats(EAST)},
   {"id":"shenzhen","name":"深圳校区","city":"深圳市光明区公常路 66 号",
    "colleges":["集成电路学院","电子与通信工程学院"],
    "rooms":rooms(SZ),"stats":stats(SZ)},
   {"id":"zhuhai","name":"珠海校区","city":"珠海市高新区唐家湾镇大学路 2 号",
    "colleges":["微电子科学与技术学院"],
    "rooms":rooms(ZH),"stats":stats(ZH)},
 ]}

HUST = {
 "school":"华中科技大学","granularity":"building",
 "audience":"研究生（该文件本身即研究生入学须知）",
 "confidence":"official","dataYear":"2024",
 "source":"https://yz.chsi.com.cn/kyzx/yxzc/202408/20240802/2293305978.html",
 "sourceLabel":"华中科技大学2024年研究生新生入学须知","sourcePage":None,
 "fetched":"2026-09-01",
 "scope":("主校区与同济校区学子苑，按原文的楼栋分组照录。"
          "原文同济校区 503 栋之后的内容在检索结果中被截断，未录入。"
          "该须知按年发布，2025/2026 版发布后需重新核对。"),
 "campuses":[
   {"id":"main","name":"主校区","city":"武汉市洪山区珞喻路 1037 号","colleges":[],
    "rooms":rooms2(HUST_MAIN),"stats":stats2(HUST_MAIN)},
   {"id":"tongji","name":"同济校区","city":"武汉市硚口区航空路 13 号","colleges":[],
    "rooms":rooms2(HUST_TJ),"stats":stats2(HUST_TJ)},
 ]}

SCUT = {
 "school":"华南理工大学","granularity":"range",
 "audience":"本科招生章程口径，未单列研究生标准",
 "confidence":"partial","dataYear":"2025",
 "source":"https://www.dxsbb.com/news/52746.html",
 "sourceLabel":"华南理工大学2025年招生章程（收费标准条款）","sourcePage":None,
 "fetched":"2026-09-01",
 "range":{"min":600,"max":1600},
 "scope":("学校只公示了住宿费区间，没有逐楼栋的公示表；且这个区间出自本科招生章程，"
          "研究生是否同一标准未见明文。要准确数字需查学校信息公开栏目或直接问研究生院。"),
 "campuses":[]}

WHU = {
 "school":"武汉大学","granularity":"range",
 "audience":"研究生","confidence":"official","dataYear":"2023",
 "source":"https://wdyz.whu.edu.cn/info/1027/3144.htm",
 "sourceLabel":"武汉大学研究生招生信息网 · 常见问题","sourcePage":None,
 "fetched":"2026-09-01",
 "range":{"min":920,"max":2480},
 "scope":("研招网答疑给的是区间，原文说明宿舍由学校统筹安排、住宿地点不同条件不同，"
          "标准经湖北省物价部门核定。页面更新于 2023 年，可能已过期。"),
 "campuses":[]}

doc = {
 "updated": "2026-09",
 "note": ("各校住宿费与宿舍条件，逐条抄自学校官方渠道（信息公开公示表 / 研究生入学须知 / "
          "招生章程），单位一律为元/生·学年，不含水电费。"
          "各校公示粒度差别很大：有的逐楼栋公示（granularity=building），"
          "有的只给一个区间（granularity=range）——本库如实保留这个差别，不去补齐。"),
 "caveats": [
   "住宿费与学费分开缴纳，招生简章里的学费不含住宿。",
   "研究生宿舍的具体分配（几人间、哪个园区）多由学校统筹安排，不是报考时能选的。",
   "各校标准按学年公示，报考当年请重新核对。",
 ],
 "schools": [SYSU, HUST, SCUT, WHU],
}

for sc in doc["schools"]:
    for c in sc.get("campuses",[]):
        c["count"] = len(c["rooms"])
    sc["count"] = sum(c["count"] for c in sc.get("campuses",[]))
    if sc["granularity"] == "range":
        sc["stats"] = {"min":sc["range"]["min"],"max":sc["range"]["max"],"bedTypes":[]}
    else:
        fees=[r["fee"] for c in sc["campuses"] for r in c["rooms"]]
        beds=sorted({r["beds"] for c in sc["campuses"] for r in c["rooms"]})
        sc["stats"]={"min":min(fees),"max":max(fees),"bedTypes":beds}

doc["total"] = sum(sc["count"] for sc in doc["schools"])
doc["schoolsCovered"] = len(doc["schools"])

# ── 覆盖缺口：院校库里有、但住宿数据还没查的学校 ──────────────
# 沿用本库对 0854 覆盖用的同一套写法：明确区分「已录入」和「还没查」，
# 不让空白看起来像是「这学校没有宿舍数据」。
_here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(_here,"data","schools.json"),encoding="utf-8") as f:
    _all = [x["name"] for x in json.load(f)["schools"]]
_done = {sc["school"] for sc in doc["schools"]}
doc["gaps"] = sorted(n for n in _all if n not in _done)
doc["coverage"] = {"covered": len(_done), "total": len(_all),
                   "note": "分母是院校库收录的学校数；缺口列表里的学校只是还没查，不代表查不到。"}

here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(here,"data","dorms.json"),"w",encoding="utf-8") as f:
    json.dump(doc,f,ensure_ascii=False,indent=1)

print(f"✓ dorms.json  {doc['schoolsCovered']} 所学校，{doc['total']} 条房型")
for sc in doc["schools"]:
    st=sc["stats"]
    g = "逐楼栋" if sc["granularity"]=="building" else "仅区间"
    print(f"   {sc['school']:<10} {g}  {st['min']}–{st['max']} 元/年  "
          f"{sc['count']} 条  conf={sc['confidence']}  {sc['dataYear']}")
