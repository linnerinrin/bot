"""
img_profile 绘制个人信息模块
"""

from io import BytesIO

from PIL import Image, ImageDraw, ImageFont

from config.Expection import LXNSRequestError, QLogoRequestError
from config.wmc_setting import wmc_settings
from core.wmc_core.db_infocr import info_load
from core.wmc_core.dv_records import get_b50
from core.wmc_core.img_material import rtframe_load


import requests
requests.packages.urllib3.disable_warnings()


def player_info(qq):
    user_info = info_load()
    record = get_b50(qq)

    FONT_RATING = ImageFont.truetype(wmc_settings.FONT_PATH, 48)

    url = f"https://q1.qlogo.cn/g?b=qq&nk={qq}&s=640"
    try:
        resp = requests.get(url)
    except Exception as e:
        raise QLogoRequestError(e)
    photo = Image.open(BytesIO(resp.content)).convert("RGBA")

    try:
        bgid = user_info[str(qq)]["plate"]
        if not bgid:
            raise Exception
    except:
        bgid = 11

    url = f"https://assets2.lxns.net/maimai/plate/{bgid}.png"
    try:
        resp = requests.get(url)
    except Exception as e:
        raise LXNSRequestError(e)
    bg = Image.open(BytesIO(resp.content)).convert("RGBA")

    nickname = record["nickname"]
    records = record["charts"]
    b35 = records["sd"]
    b15 = records["dx"]
    sdrt = 0
    dxrt = 0
    for sd in b35:
        sdrt += sd["ra"]
    for dx in b15:
        dxrt += dx["ra"]
    rt = sdrt + dxrt

    if rt < 1000:
        rtf = rtframe_load("0")
    elif rt < 2000:
        rtf = rtframe_load("1000")
    elif rt < 4000:
        rtf = rtframe_load("2000")
    elif rt < 7000:
        rtf = rtframe_load("4000")
    elif rt < 10000:
        rtf = rtframe_load("7000")
    elif rt < 12000:
        rtf = rtframe_load("10000")
    elif rt < 13000:
        rtf = rtframe_load("12000")
    elif rt < 14000:
        rtf = rtframe_load("13000")
    elif rt < 14250:
        rtf = rtframe_load("14000")
    elif rt < 14500:
        rtf = rtframe_load("14250")
    elif rt < 14750:
        rtf = rtframe_load("14500")
    elif rt < 15000:
        rtf = rtframe_load("14750")
    elif rt < 15250:
        rtf = rtframe_load("15000")
    elif rt < 15500:
        rtf = rtframe_load("15250")
    elif rt < 15750:
        rtf = rtframe_load("15500")
    elif rt < 16000:
        rtf = rtframe_load("15750")
    elif rt < 16250:
        rtf = rtframe_load("16000")
    elif rt < 16500:
        rtf = rtframe_load("16250")
    elif rt < 16750:
        rtf = rtframe_load("16500")
    else:
        rtf = rtframe_load("16750")

    photo = photo.resize((250, 250))
    rtf = rtf.resize((440, 80))
    bg = bg.resize((1800, 290))

    card = bg
    draw = ImageDraw.Draw(card)
    card.paste(bg, (0, 0), mask=bg)
    card.paste(photo, (20, 20))
    card.paste(rtf, (360, 20), mask=rtf)
    for idx, string in enumerate(str(rt)):
        draw.text((565 + idx * 35, 25), string, fill=(255, 215, 0), font=FONT_RATING)
    draw.rounded_rectangle([360, 120, 700, 180], radius=15, outline=(0, 0, 0), width=1, fill=(255, 255, 255))
    draw.text((380, 125), f"{nickname}", font_size=36, fill=(0, 0, 0))
    draw.rounded_rectangle([360, 210, 800, 240], radius=15, outline=(0, 0, 0), fill=(255, 255, 255), width=1)
    draw.text((380, 210), f"Best35:{sdrt} + Best15:{dxrt} = {rt}", font_size=24, fill=(0, 0, 0))
    return card





