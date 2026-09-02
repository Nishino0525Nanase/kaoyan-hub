# -*- coding: utf-8 -*-
"""
补入南京大学电子科学与工程学院的专业记录。

库里原有的 7 条南大记录全在计算机口（计算机学院、软件学院、人工智能学院等），
电子科学与工程学院一条都没有——正是硬件方向的缺口。

数据来源：
  《电子科学与工程学院2026年硕士研究生复试笔试参考书目》(官网 PDF)
  https://ese.nju.edu.cn/9e/34/c22673a826932/page.htm 的附件

这份 PDF 给出的是**专业清单 + 复试笔试参考书目**，是官方原文，confidence=official。
它不含初试科目，所以 subjects 一律留 null——不从别处推测、不拿聚合站的数据混进来。
初试科目待后续从学校专业目录单独核实。
"""
import json, os

D = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
P = os.path.join(D, "programs.json")
doc = json.load(open(P, encoding="utf-8"))

SRC = "https://ese.nju.edu.cn/9e/34/c22673a826932/page.htm"
PDF = ("https://ese.nju.edu.cn/_upload/article/files/30/c3/d5d8b0354ec989b506083ccbef81/"
       "4c0167ff-9f5c-46e1-9ad5-d12b868dd6a9.pdf")
COLLEGE = "电子科学与工程学院"

B_EM = ["《电磁场理论与微波技术》(第二版) 伍瑞新、冯一军等，南京大学出版社",
        "《大学物理学》(电磁学、光学部分) 张三慧主编，清华大学出版社"]
B_SEMI = ["《半导体物理学》刘恩科、朱秉升、罗晋生等，国防工业出版社",
          "《半导体器件物理》施敏著，赵鹤鸣等译，苏州大学出版社"]
B_DIP = ["《数字图像处理》(原书第3版) Gonzalez & Woods，阮秋琦、阮宇智译，电子工业出版社"]
B_COMM = ["《通信原理》樊昌信、曹丽娜，国防工业出版社"]
B_SIG = ["《电路》(第六版) 邱关源、罗先觉，高等教育出版社",
         "《数字逻辑基础与Verilog设计》(原书第3版) Brown & Vranesic，机械工业出版社",
         "《数字电子技术基础》(第三版) 阎石主编，高等教育出版社"]
B_C85402 = ["《数字逻辑基础与Verilog设计》(原书第3版) Brown & Vranesic，机械工业出版社",
            "《数字电子技术基础》(第五版) 阎石主编，高等教育出版社",
            "《模拟电子技术基础》(第七版) 康华光主编，高等教育出版社"]

# (代码, 名称, 学位类型, 复试参考书)
ROWS = [
 ("070208", "无线电物理",                       "学硕", B_EM),
 ("080904", "电磁场与微波技术",                   "学硕", B_EM),
 ("080901", "物理电子学",                       "学硕", B_SEMI),
 ("080903", "微电子学与固体电子学",                 "学硕", B_SEMI),
 ("080902", "电路与系统",                       "学硕", B_DIP),
 ("081001", "通信与信息系统",                     "学硕", B_COMM),
 ("081002", "信号与信息处理",                     "学硕", B_SIG),
 ("085403", "集成电路工程",                      "专硕", B_SEMI),
 ("085402", "通信工程（含宽带网络、移动通信等）",          "专硕", B_C85402),
]

proto = doc["records"][0]
added = 0
for code, name, degree, books in ROWS:
    if any(r["school"] == "南京大学" and r["code"] == code and r["college"] == COLLEGE
           for r in doc["records"]):
        continue
    # 数组型字段按既有约定初始化为 []，写 null 会让渲染端的 r.lines[0] 直接抛异常
    rec = {k: ([] if isinstance(proto[k], list) else None) for k in proto}
    rec.update({
        "school": "南京大学",
        "track": "ee",
        "code": code,
        "name": name,
        "college": COLLEGE,
        "degree": degree,
        "subjects": [],            # 该 PDF 不含初试科目；用 [] 而非 None，渲染端按数组处理
        # 注意：既有的 retest 字段一半是 int(复试录取人数)、一半是 dict，
        # 语义已经混了，这里不去覆盖它，复试参考书另开字段。
        "retestBooks": books,
        "sources": [{"url": SRC, "official": True},
                    {"url": PDF, "official": True}],
        "confidence": "official",
        "note": ("来源为学院《2026年硕士研究生复试笔试参考书目》，"
                 "含专业清单与复试参考书；初试科目该文件未列出，待单独核实"),
    })
    doc["records"].append(rec)
    added += 1

# 重算完整度
from collections import defaultdict
agg = defaultdict(lambda: {"n": 0, "sub": 0, "line": 0})
for r in doc["records"]:
    a = agg[r["school"]]; a["n"] += 1
    if r.get("subjects"): a["sub"] += 1
    if r.get("lines") or r.get("line"): a["line"] += 1
doc["completeness"]["bySchool"] = {k: v for k, v in sorted(agg.items())}
doc["completeness"]["totals"] = {
    "records": len(doc["records"]),
    "withSubjects": sum(1 for r in doc["records"] if r.get("subjects")),
    "withLines": sum(1 for r in doc["records"] if r.get("lines") or r.get("line")),
    "withRetestBooks": sum(1 for r in doc["records"] if r.get("retestBooks")),
}

json.dump(doc, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"✓ 南大电科院 +{added} 条")
print("  南大合计:", agg["南京大学"])
print("  全库:", doc["completeness"]["totals"])
