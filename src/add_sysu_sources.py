# -*- coding: utf-8 -*-
"""
在资料链接页新增「中山大学官方信源」分组。
全部为学校/学院官网直链，均经抓取验证可访问（知乎等二手转述不收）。
"""
import json, os
D = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
P = os.path.join(D, "resources.json")
doc = json.load(open(P, encoding="utf-8"))

GROUP = {
 "title": "中山大学官方信源",
 "desc": "全部为学校 / 学院官网直链。招生政策以这些页面为准，二手转述一律核对原文",
 "links": [
  {"name":"中山大学研究生招生网",
   "url":"https://graduate.sysu.edu.cn/zsw/",
   "desc":"简章、专业目录、复试线、调剂公告的唯一官方发布渠道。2027 级简章预计 2026 年 9 月发布"},
  {"name":"研招网 · 招生章程栏目",
   "url":"https://graduate.sysu.edu.cn/zsw/admissions-regulations",
   "desc":"历年招生章程原文，可对比推免比例与统考名额的逐年变化"},
  {"name":"2026 年硕士招生学科专业目录（PDF）",
   "url":"https://graduate.sysu.edu.cn/zsw/sites/default/files/2025-09/2%E3%80%81%E4%B8%AD%E5%B1%B1%E5%A4%A7%E5%AD%A62026%E5%B9%B4%E7%A1%95%E5%A3%AB%E7%A0%94%E7%A9%B6%E7%94%9F%E6%8B%9B%E7%94%9F%E5%AD%A6%E7%A7%91%E4%B8%93%E4%B8%9A%E7%9B%AE%E5%BD%95.pdf",
   "desc":"全校逐专业的初试科目、复试专业课与拟招生人数。本库中大数据即出自此件"},
  {"name":"2025 年硕士复试基本分数线（PDF）",
   "url":"https://graduate.sysu.edu.cn/zsw/sites/default/files/2025-03/%E4%B8%AD%E5%B1%B1%E5%A4%A7%E5%AD%A62025%E5%B9%B4%E7%A1%95%E5%A3%AB%E7%A0%94%E7%A9%B6%E7%94%9F%E6%8B%9B%E7%94%9F%E8%80%83%E8%AF%95%E5%A4%8D%E8%AF%95%E5%9F%BA%E6%9C%AC%E5%88%86%E6%95%B0%E7%BA%BF_0.pdf",
   "desc":"校线。原文注明各招生单位可在校线之上自定院线，故院线往往更高"},
  {"name":"学生宿舍住宿费收费标准公示表（信息公开网）",
   "url":"https://xxgk.sysu.edu.cn/cat/122",
   "desc":"逐楼栋的房型、面积、住宿费。网页要登录，但 PDF 附件可直接下载"},
  {"name":"报考点 4413 赴考须知",
   "url":"https://graduate.sysu.edu.cn/zsw/article/474",
   "desc":"选中大报考点时看，含南校园与东校园考场位置图"},
  {"name":"研究生招生平台（复试材料提交）",
   "url":"https://enroll.sysu.edu.cn/",
   "desc":"复试资格审查材料统一在此提交，各学院细则均指向该系统"},
  {"name":"电子与信息工程学院（微电子学院）· 广州东校园",
   "url":"https://seit.sysu.edu.cn/",
   "desc":"085403 拟招 81 人，规模最大。2025 复试细则见 seit.sysu.edu.cn/article/2746"},
  {"name":"微电子科学与技术学院 · 珠海校区",
   "url":"https://mst.sysu.edu.cn/admission",
   "desc":"复试为纯面试无笔试。2025 院线 336，总计划 34 但推免占 23、统考仅 11"},
  {"name":"集成电路学院 · 深圳校区",
   "url":"https://sic.sysu.edu.cn/rc/rc05/index.htm",
   "desc":"复试含闭卷专业课笔试（模电 + 数电 + 半导体物理），复试总分 500 占 50%"},
  {"name":"电子与通信工程学院 · 深圳校区",
   "url":"https://sece.sysu.edu.cn/zs/zs01/index.htm",
   "desc":"085400 拟招 80 人，专业课考 884 信号与系统。含研究生导师招生专业方向情况表"},
 ]}

doc["groups"] = [g for g in doc["groups"] if g["title"] != GROUP["title"]]
# 插在「官方必看」之后
idx = next((i for i, g in enumerate(doc["groups"]) if g["title"] == "官方必看"), 0)
doc["groups"].insert(idx + 1, GROUP)
doc["updated"] = "2026-09"
json.dump(doc, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"✓ 资料链接新增「{GROUP['title']}」{len(GROUP['links'])} 条")
print("  分组:", [g["title"] for g in doc["groups"]])
