"""
img_cover.py 获得所需歌曲封面
get_cover_image() 获得指定[reid(索引)]歌曲封面
"""

from PIL import Image

from config.wmc_setting import wmc_settings
import requests
requests.packages.urllib3.disable_warnings()


def get_cover_image(image_reid):
    try:
        img = Image.open(wmc_settings.WMC_MATERIAL_COVER + f"{image_reid}.png")
        return img
    except:
        return Image.new("RGB", (160, 160), (200, 200, 200))

