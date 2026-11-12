"""
用于加载绘图素材模块

"""

from PIL import Image

from config.Expection import NoRescourseError
from config.wmc_setting import wmc_settings


def version_title_load(ver):
    ver = wmc_settings.VERSION_PNG[ver]
    try:
        img = Image.open(wmc_settings.WMC_MATERIAL + f"{ver}").convert("RGBA").resize((150, 75))
        return img
    except Exception as e:
        raise NoRescourseError(e)



def dx_load(s):
    try:
        if s == "std":
            img = Image.open(wmc_settings.WMC_MATERIAL_DX + "std.png").convert("RGBA").resize((70, 25))
            return img
        if s == "dx":
            img = Image.open(wmc_settings.WMC_MATERIAL_DX + "dx.png").convert("RGBA").resize((70, 25))
            return img
    except Exception as e:
        raise NoRescourseError(e)


def sss_load(s):
    try:
        img = Image.open(wmc_settings.WMC_MATERIAL_SSS + f"{s}.png").convert("RGBA")
        return img
    except Exception as e:
        raise NoRescourseError(e)

def rtframe_load(s):
    try:
        img = Image.open(wmc_settings.WMC_MATERIAL_RT + f"{s}.png").convert("RGBA")
        return img
    except Exception as e:
        raise NoRescourseError(e)

def star_load(s):
    try:
        img = Image.open(wmc_settings.WMC_MATERIAL_STAR + f"{s}.png").convert("RGBA")
        return img
    except Exception as e:
        raise NoRescourseError(e)

def fc_load(s):
    try:
        img = Image.open(wmc_settings.WMC_MATERIAL_FC + f"{s}.png").convert("RGBA")
        return img
    except Exception as e:
        raise NoRescourseError(e)


def fdx_load(s):
    try:
        img = Image.open(wmc_settings.WMC_MATERIAL_FDX + f"{s}.png").convert("RGBA")
        return img
    except Exception as e:
        raise NoRescourseError(e)
