
"""

通过b链获取视频信息的函数

merge_vide_audio 使用moviepy合并下载到的视频与音频文件
_download_file 使用获得到的url下载文件
do_download 根据bv号下载视频 <-可以新加登录以获取更高清晰度下载的功能 但是他妈估计要写一整个登录逻辑还有存储读取维护 不过考虑过我写过 其实也可以加上
analysis_bili 根据输入的cq信息获得视频基本信息 并决定是否下载与输出视频

"""

import os

from config.Expection import BiliRequestError,BiliVideoTimeoutError,BiliVideoDownloadError
from config.regular_setting import regular_settings
from core.regular_core.bili_analysis import bili_analysis
from core.regular_core.bili_video_download import do_download
from nonebot.adapters.onebot.v11 import MessageSegment

from utils.error import error_output

LIMIT_MIN=regular_settings.LIMIT_MIN
DOC_DIR=regular_settings.bili_mount
async def bili(handler,msg):
    try:
        bvid,info=await bili_analysis(msg)
    except BiliRequestError as e:
        await error_output(handler,e)
        return
    title = info["title"]
    up = info["owner"]["name"]
    desc = info["desc"]
    view = info["stat"]["view"]
    good = info["stat"]["like"]
    coin = info["stat"]["coin"]
    sc = info["stat"]["favorite"]
    picurl = info["pic"]
    await handler.send(MessageSegment.image(picurl) + f"""\n
    📺 标题：{title}\n👤 UP主：{up}\n📝 简介：{desc[:150]}...\n👁 播放：{view}\n👍 点赞：{good}\n🪙 投币：{coin}\n⭐ 收藏：{sc}
    """.strip())
    try:
        path = await do_download(bvid,LIMIT_MIN*60)
    except BiliVideoTimeoutError:
        await handler.finish(f"超过{LIMIT_MIN}分钟的视频就不要浪费大家时间了！")
        return
    except BiliVideoDownloadError as e:
        await error_output(handler,e)
        return
    await handler.send(MessageSegment.video(f"file:///{DOC_DIR}{bvid}.mp4"))
    os.remove(path)
    await handler.finish()

