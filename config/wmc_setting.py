import os
from typing import List, Tuple, Dict

from pydantic_settings import BaseSettings, SettingsConfigDict

from config.global_setting import global_setting


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file="wmc.env", extra="ignore")

    LOCAL_PATH:str=global_setting.local_path
    MOUNT_PATH:str=global_setting.mount_path

    VERSION_PNG: Dict
    CANVAS_W: int
    CANVAS_H: int
    BG_COLOR: Tuple
    TEXT_COLOR: Tuple
    LINE_COLOR: Tuple

    DIFF_INDEX: Dict
    DIFF_COLOR: List[Tuple]

    @property
    def DB_LOCAL(self):
        return rf"{self.WMC_DATASET}dxdata.csv"

    @property
    def WMC_DATASET(self):
        return rf"{self.LOCAL_PATH}/data/wmc/datasets/"

    @property
    def WMC_MATERIAL(self):
        return rf"{self.LOCAL_PATH}/data/wmc/materials/version-title/"

    @property
    def WMC_MATERIAL_BG(self):
        return rf"{self.LOCAL_PATH}/data/wmc/materials/version-bg/"

    @property
    def WMC_MATERIAL_DX(self):
        return rf"{self.LOCAL_PATH}/data/wmc/materials/isdx/"

    @property
    def WMC_MATERIAL_SSS(self):
        return rf"{self.LOCAL_PATH}/data/wmc/materials/ev/"

    @property
    def WMC_MATERIAL_RT(self):
        return rf"{self.LOCAL_PATH}/data/wmc/materials/rtframe/"

    @property
    def WMC_MATERIAL_STAR(self):
        return rf"{self.LOCAL_PATH}/data/wmc/materials/star/"

    @property
    def WMC_MATERIAL_FC(self):
        return rf"{self.LOCAL_PATH}/data/wmc/materials/isfc/"

    @property
    def WMC_MATERIAL_FDX(self):
        return rf"{self.LOCAL_PATH}/data/wmc/materials/isfdx/"

    @property
    def WMC_MATERIAL_COVER(self):
        return rf"{self.LOCAL_PATH}/data/wmc/materials/covers/"

    @property
    def WMC_MATERIAL_PLATE(self):
        return rf"{self.LOCAL_PATH}/data/wmc/materials/plate"

    @property
    def EXTRA_JSON(self):
        return rf"{self.WMC_DATASET}extra.json"

    @property
    def FONT_PATH(self):
        return rf"{self.LOCAL_PATH}/data/Fonts/msyhbd.ttc"

    @property
    def USERINFO_JSON(self):
        return rf"{self.WMC_DATASET}userinfo.json"


wmc_settings = Config()