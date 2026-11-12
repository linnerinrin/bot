
"""
获取/更新乐曲封面的函数集合
get_cover_image 在dxrating.net上获取封面
get_cover_image_byurl 用于手动获取get_cover_image_mutil获取失败的封面
get_cover_image_byurl 尝试获取dxrating.csv中所有乐曲封面

"""

import csv
import os
from io import BytesIO
import requests as requests
requests.packages.urllib3.disable_warnings()
import requests
from PIL import Image

base_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(os.path.dirname(base_dir))
os.makedirs(rf"{project_dir}/wmc/materials/covers/",exist_ok=True)

def load_songs(csv_path):
    songs = []
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append(row)
    return songs

def get_cover_image(image_name):
    try:
        url = f"https://shama.dxrating.net/images/cover/v2/{image_name}.jpg"
        resp = requests.get(url, timeout=20,verify=False)
        img = Image.open(BytesIO(resp.content)).convert("RGB")
        img = img.resize((160, 160), Image.Resampling.LANCZOS)
        return img
    except Exception as e:
        print(e)

def get_cover_image_byurl(url,reid):
    try:
        resp = requests.get(url, timeout=20,verify=False)
        img = Image.open(BytesIO(resp.content)).convert("RGB")
        img = img.resize((160, 160), Image.Resampling.LANCZOS)
        try: img.save(rf"{project_dir}/wmc/materials/covers/{reid}.png", "PNG")
        except:...
    except Exception as e:
        print(e)

def get_cover_image_mutil():
    songs = load_songs(r"dxdata.csv")
    for song in songs:
        if not os.path.exists(rf"{project_dir}/wmc/materials/covers/{song['索引']}.png"):
            cov=get_cover_image(song["封面"])
            try:cov.save(rf"{project_dir}/wmc/materials/covers/{song['索引']}.png","PNG")
            except:...
            print(song["索引"]," ",song["曲名"])


get_cover_image_mutil()
get_cover_image_byurl("https://static.wikia.nocookie.net/maimai/images/7/7b/202603051_mms_breakthespeakers.png/revision/latest?cb=20260309033309&path-prefix=zh",
                      191)