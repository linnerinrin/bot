"""
db_songs.py 乐曲相关
load_songs() 加载乐曲数据库
search_songs() 关键词搜索

"""

import csv
import json

from config.wmc_setting import wmc_settings

with open(wmc_settings.EXTRA_JSON, "r", encoding="utf-8") as f:
    extra = json.load(f)


def load_songs(csv_path):
    songs = []
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append(row)
    return songs


songs = load_songs(wmc_settings.DB_LOCAL)

def search_song(keyword):
    keyword = keyword.strip().lower()
    result = []

    for s in songs:
        sid = s["internalId"].strip().lower()
        if keyword == '?':
            break
        if keyword == sid:
            return [s]

    for s in songs:
        title = s["曲名"].strip().lower()
        if keyword == title:
            result.append(s)

    for s in songs:
        alias_list = s["别名"].strip().lower().split(" \\ ")
        if keyword in alias_list:
            if s not in result:
                result.append(s)

    return result

def multi_output(result):
    if len(result) == 0:
        return "未找到该曲目！"
    selectstr = "您想寻找的可能是:\n"
    for s in result:
        selectstr += f"{s['internalId']} {s['曲名']}\n"
    selectstr += "(=^･ω･^=)直接通过id查找就好啦~"
    return selectstr
