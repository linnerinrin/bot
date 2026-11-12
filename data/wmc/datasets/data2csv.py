
"""
将 dxrting.json 与 alias.json 合并为dxrting.csv
"""

import json
import csv
from collections import defaultdict

with open("dxdata.json", "r", encoding="utf-8") as f:
    data = json.load(f)

with open("aliases.json", "r", encoding="utf-8") as f:
    aliases = json.load(f)

with open("dxdata.csv", "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)

    header = [
        "索引",
        "internalId",
        "类型",
        "版本",
        "曲名",
        "别名",
        "曲师",
        "BPM",
        "封面",
        "分类",
        "JP", "INT", "USA", "CN",

        "BASIC_定数", "BASIC_谱师", "BASIC_TAP", "BASIC_HOLD", "BASIC_SLIDE", "BASIC_TOUCH", "BASIC_BREAK", "BASIC_TOTAL", "BASIC_定数变更",
        "ADV_定数", "ADV_谱师", "ADV_TAP", "ADV_HOLD", "ADV_SLIDE", "ADV_TOUCH", "ADV_BREAK", "ADV_TOTAL", "ADV_定数变更",
        "EXP_定数", "EXP_谱师", "EXP_TAP", "EXP_HOLD", "EXP_SLIDE", "EXP_TOUCH", "EXP_BREAK", "EXP_TOTAL", "EXP_定数变更",
        "MST_定数", "MST_谱师", "MST_TAP", "MST_HOLD", "MST_SLIDE", "MST_TOUCH", "MST_BREAK", "MST_TOTAL", "MST_定数变更",
        "REM_定数", "REM_谱师", "REM_TAP", "REM_HOLD", "REM_SLIDE", "REM_TOUCH", "REM_BREAK", "REM_TOTAL", "REM_定数变更",
    ]
    w.writerow(header)

    index=0
    for song in data["songs"]:
        # 共用信息z`
        title      = song.get("title", "")
        artist     = song.get("artist", "")
        bpm        = song.get("bpm", "")
        image      = song.get("imageName", "")
        category   = song.get("category", "")
        sheets     = song.get("sheets", [])
        alias_list=song.get("searchAcronyms",[])
        try:alias_list.extend(aliases[title])
        except:...
        alias=""
        for ali in alias_list:
            alias+=ali+" \ "
        alias=alias[:-3]

        # 按 type 分成两组：std / dx
        type_groups = defaultdict(list)
        for s in sheets:
            t = s.get("type")
            if t in ("std", "dx"):
                type_groups[t].append(s)

        # 每种类型输出独立一行
        for mode, group in type_groups.items():
            index += 1
            first = group[0]
            internalId = first.get("internalId", "？")
            version    = first.get("version", "")

            # 服务器
            jp = intl = usa = cn = ""
            for s in group:
                reg = s.get("regions", {})
                if reg.get("jp"): jp = "√"
                if reg.get("intl"): intl = "√"
                if reg.get("usa"): usa = "√"
                if reg.get("cn"): cn = "√"

            empty = [""] * 9
            basic = adv = exp = mst = rem = empty

            for s in group:
                diff = s.get("difficulty")
                ilv  = s.get("internalLevelValue", "")
                des  = s.get("noteDesigner", "")
                nc   = s.get("noteCounts", {})

                tap   = nc.get("tap", "")
                hold  = nc.get("hold", "")
                slide = nc.get("slide", "")
                touch = nc.get("touch")
                touch = touch if touch is not None else "-"
                brk   = nc.get("break", "")
                total = nc.get("total", "")

                multi = s.get("multiverInternalLevelValue", {})
                multi_str = str(multi) if multi else ""

                row = [ilv, des, tap, hold, slide, touch, brk, total, multi_str]

                if diff == "basic":      basic = row
                elif diff == "advanced": adv = row
                elif diff == "expert":   exp = row
                elif diff == "master":   mst = row
                elif diff == "remaster": rem = row

            # 写入一行
            full_row = [index,
                internalId, mode, version,
                title, alias,artist, bpm, image, category,
                jp, intl, usa, cn,
                *basic, *adv, *exp, *mst, *rem
            ]
            w.writerow(full_row)


print("导出完成")