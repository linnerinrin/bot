"""
dv_records.py 从水鱼查分器获取数据
get_b50 获取best50数据 无需token
get_full_grade 获取完整数据 需token

"""

import requests

from config.Expection import DivingFishRequestError

requests.packages.urllib3.disable_warnings()


def get_b50(qq):
    headers = {"qq": qq, "b50": "1"}
    url = "https://www.diving-fish.com/api/maimaidxprober/query/player"
    resp = requests.post(url, json=headers, verify=False)
    if not resp.json():
        raise DivingFishRequestError
    return resp.json()


def get_full_grade(token):
    headers = {"Import-Token": token}
    url = "https://www.diving-fish.com/api/maimaidxprober/player/records"
    resp = requests.get(url, headers=headers, verify=False)
    if not resp.json():
        raise DivingFishRequestError
    return resp.json()
