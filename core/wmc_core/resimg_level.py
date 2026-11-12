"""
resimg_level.py 绘制指定等级图片

"""

import random

from PIL import ImageDraw

from core.wmc_core.db_infocr import info_load
from core.wmc_core.db_song import search_song, songs
from core.wmc_core.dv_records import get_full_grade
from core.wmc_core.img_cover import get_cover_image
from core.wmc_core.img_draw import paste_single, paste_me
from core.wmc_core.img_profile import player_info
from utils.set_blur_to_image import set_blur_to_image


def paste_level(qq, keys, index):
    if not index:
        index = 1
    index = int(index)
    valid_levels = ["1", "2", "3", "4", "5", "6", "7", "8", "8+", "9", "9+", "10", "10+", "11", "11+", "12", "12+", "13", "13+", "14", "14+", "15"]
    if keys not in valid_levels:
        return 2, "没有这个等级哦"

    user_info = info_load()
    import_token = user_info[str(qq)]["token"]
    records = get_full_grade(import_token)["records"]
    top = player_info(qq)

    record = [r for r in records if r["level"] == f"{keys}"]
    record = sorted(record, key=lambda x: x["achievements"], reverse=True)
    length = len(record)
    if length < 50 * index - 50:
        return 2, "索引超长"

    b50 = record[50 * index - 50:50 * index]
    b50_pic = []

    bg = None
    try:
        bg = get_cover_image(user_info[str(qq)]["bg"])
        if not bg:
            raise Exception
    except Exception as e:
        print(e)
        max_song = None
        maxrt = 0
        for single in b50:
            if single["ra"] > maxrt:
                maxrt = single["ra"]
                max_song = single
        try:
            bg = get_cover_image(search_song(max_song["title"])[0]["索引"])
        except:
            bg = get_cover_image(songs[random.randint(0, len(songs) - 1)]["索引"])

    for single in b50:
        b50_pic.append(paste_single(single))

    card = set_blur_to_image(bg, bg_size=(1800, 2400))
    draw = ImageDraw.Draw(card)

    x_s = 100
    y_s = 420
    wid = 300
    hei = 150
    cols = 5
    rows = 10
    x_int = 20
    y_int = 25
    card.paste(top, (0, 0))

    for row in range(rows):
        y = y_s + row * (y_int + hei)
        for col in range(cols):
            try:
                card.paste(b50_pic[row * 5 + col], (x_s + col * (x_int + wid), y), mask=b50_pic[row * 5 + col])
            except:
                continue
    paste_me(draw, (1800, 2400), 36)
    return 1, card
