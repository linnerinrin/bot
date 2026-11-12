"""
通过dxrting.net 接口获取乐曲别名的
"""


import json
from collections import defaultdict

import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://miruku.dxrating.net/api/v1/aliases"

headers = {
    "Host": "miruku.dxrating.net",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Origin": "https://dxrating.net",
    "Referer": "https://dxrating.net/",
}

resp = requests.get(url, headers=headers, verify=False, timeout=15)

aliases=resp.json()
alias_map = defaultdict(list)
for item in aliases:
    song_id = item["song_id"]
    name = item["name"]
    alias_map[song_id].append(name)

alias_list = {}
for key, item_list in alias_map.items():
    alias_list[key]=(item_list)

with open("data/wmc/aliases.json", "w", encoding="utf-8") as f:
    json.dump(alias_list, f, ensure_ascii=False, indent=2)