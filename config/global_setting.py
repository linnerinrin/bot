import os
from typing import List, Tuple

from pydantic_settings import BaseSettings,SettingsConfigDict

class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file="global.env", extra="ignore")


    MODE:str="BLACK"
    BLACK:List
    WHITE:List


    @property
    def local_path(self):
        #本地项目根路径 通过dirname寻找 用于nonebot出发的本地文件操作
        base_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.dirname(base_dir)
        return project_dir

    @property
    def mount_path(self):
        #挂载项目根路径 硬编码 用于napcat出发的docker文件操作
        return 'app/data'


global_setting=Config()