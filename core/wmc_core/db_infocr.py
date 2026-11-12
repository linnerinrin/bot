"""
db_infocr.py 用于加载用户个性化设置数据库的函数
info_load 加载数据库
info_dump 写入用户指定的数据

"""

import json

from config.wmc_setting import wmc_settings

empty_dict = {"token": None, "bg": None, "plate": None}


def info_load():
    with open(wmc_settings.USERINFO_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def info_dump(user_info, uid, cmd, tid):
    if str(uid) not in user_info:
        user_info[str(uid)] = empty_dict
    user_info[str(uid)][cmd] = tid
    with open(wmc_settings.USERINFO_JSON, "w", encoding="utf-8") as f:
        json.dump(user_info, f, ensure_ascii=False, indent=2)
