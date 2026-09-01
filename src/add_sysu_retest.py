# -*- coding: utf-8 -*-
"""
把中山大学电子与信息工程学院（微电子学院）2025 年复试录取实施细则
写进 quota-retest.json。字段沿用该文件已有的 schema，不新造结构。
数据全部来自 https://seit.sysu.edu.cn/article/2746 原文。
"""
import json, os

D = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
P = os.path.join(D, "quota-retest.json")
doc = json.load(open(P, encoding="utf-8"))

SRC = "https://seit.sysu.edu.cn/article/2746"
COLLEGE = "电子与信息工程学院（微电子学院）"

# 复试构成三部分对所有专业一致，抽出来共用
RETEST = {
    "ratio": None,
    "weight": "总成绩 = 初试成绩 + 复试成绩，两者各占 50%（初试满分 500，复试满分 500）",
    "hasMachineTest": False,
    "subjects": ("专业课笔试 100 分（科目见招生专业目录的复试专业课，闭卷）"
                 " + 外语应用能力测试 100 分"
                 " + 专业能力及综合素质考核 300 分（与外语测试合并为现场面试，每人不少于 20 分钟）"),
    "passLine": "复试成绩低于满分 60%（即低于 300 分）为不合格，不予录取",
    "tieBreak": "总成绩同分先比初试成绩；初试再同分则比复试专业课笔试成绩",
    "form": "现场复试，笔试 + 面试",
}

# (专业代码, 专业名称, 总计划, 已招推免, 公开招考, 复试线总分, 政治, 外语, 业务课一, 业务课二, track)
ROWS = [
 ("080300","光学工程",                    19,  8, 11, 280, 45, 45, 60, 60, "ee"),
 ("080900","电子科学与技术",                20, 15,  5, 300, 45, 45, 60, 60, "ee"),
 ("081000","信息与通信工程",                19, 11,  8, 280, 45, 45, 60, 60, "ee"),
 ("085402","通信工程（含宽带网络、移动通信等）",   22,  9, 13, 320, 50, 50, 60, 60, "ee"),
 ("085403","集成电路工程",                 82, 28, 54, 340, 50, 50, 60, 60, "ee"),
 ("085408","光电信息工程",                 22,  7, 15, 320, 50, 50, 60, 60, "ee"),
]

added = 0
for code, name, total, tm, exam, ln, pol, eng, c1, c2 in [(r[0],r[1],r[2],r[3],r[4],r[5],r[6],r[7],r[8],r[9]) for r in ROWS]:
    track = "ee"
    key = ("中山大学", code, COLLEGE)
    if any((r["school"], r["code"], r["college"]) == key for r in doc["records"]):
        continue
    doc["records"].append({
        "school": "中山大学",
        "track": track,
        "code": code,
        "name": name,
        "college": COLLEGE,
        "quota": {
            "year": 2025,
            "planTotal": total,
            "tuimian": tm,
            "exam": exam,
            "tuimianRatio": round(tm / total, 3),
            "note": ("复试细则原文直接给出「总计划 / 已招推免生 / 公开招考计划」三列，"
                     "统考数为官方公布值，非推算。原文注明最终以实际录取人数为准"),
        },
        "retest": dict(RETEST),
        "line": {
            "year": 2025,
            "total": ln, "politics": pol, "english": eng,
            "course1": c1, "course2": c2,
            "note": "学院复试分数线（院线），不分方向",
        },
        "sources": [{"url": SRC, "official": True}],
        "confidence": "official",
    })
    added += 1

doc["updated"] = "2026-09"
json.dump(doc, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"✓ quota-retest.json 新增 {added} 条，现共 {len(doc['records'])} 条")
for r in doc["records"][-added:]:
    q = r["quota"]
    print(f"   {r['code']} {r['name'][:18]:<18} 计划{q['planTotal']:>3} "
          f"推免{q['tuimian']:>3} 统考{q['exam']:>3} 院线{r['line']['total']}")
