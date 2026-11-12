"""
用于给wmc_message插件提供服务
db_alias 查询歌曲别名
db_cover 输出歌曲封面
db_single_info 输出歌曲单曲信息卡片
dv_best50 水鱼获取b50
dv_bgset 设置输出玩家信息的背景图片 用歌曲封面 并存储
dv_bind 绑定玩家的水鱼查分器 并存储
dv_followlevel_grade 水鱼获取全部数据 并取指定等级数据 




前缀db表示直接从本地乐曲数据库获得数据
前缀dv表示从水鱼查分器里获取数据 大部分功能需要提供水鱼token
"""