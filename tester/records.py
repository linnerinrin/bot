
"""

用于调用水鱼等接口获取玩家成绩的函数集合

get_b50 获取玩家简略成绩
get_full_grade 获取玩家详细成绩
"""

import requests
requests.packages.urllib3.disable_warnings()
import json

def get_b50(qq):
    headers = {
        "qq": qq,
        "b50": "1"
    }
    url = "https://www.diving-fish.com/api/maimaidxprober/query/player"
    resp = requests.post(url, json=headers,verify=False)
    records = resp.json()
    return records

def get_full_grade(token):
    headers = {
        "Import-Token": token,
    }
    url = "https://www.diving-fish.com/api/maimaidxprober/player/records"
    resp = requests.get(url, headers=headers, verify=False)
    records=resp.json()
    return records
