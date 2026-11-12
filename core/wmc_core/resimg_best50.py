"""
resimg_best50.py 绘制best50图片
"""

import random

from PIL import ImageDraw

from core.wmc_core.db_infocr import info_load
from core.wmc_core.db_song import search_song, songs
from core.wmc_core.dv_records import get_b50
from core.wmc_core.img_cover import get_cover_image
from core.wmc_core.img_draw import paste_single, paste_me

from core.wmc_core.img_profile import player_info
from utils.set_blur_to_image import set_blur_to_image


def paste_b50(qq):
    user_info = info_load()
    record = get_b50(qq)
    top = player_info(qq)
    records = record["charts"]
    b15 = records["dx"]
    b35 = records["sd"]
    b50 = b15 + b35
    b35_pic = []
    b15_pic = []

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

    for single in b35:
        b35_pic.append(paste_single(single))
    for single in b15:
        b15_pic.append(paste_single(single))

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
        if row <= 6:
            for col in range(cols):
                try:
                    card.paste(b35_pic[row * 5 + col], (x_s + col * (x_int + wid), y), mask=b35_pic[row * 5 + col])
                except:
                    continue
        elif row > 6:
            y += 100
            for col in range(cols):
                try:
                    card.paste(b15_pic[row * 5 + col - 35], (x_s + col * (x_int + wid), y), mask=b15_pic[row * 5 + col - 35])
                except:
                    continue
    paste_me(draw, (1800, 2400), 36)
    return card