import re

from service.wmc_service.db_alias import get_alias
from service.wmc_service.db_cover import get_cover
from service.wmc_service.db_single_info import get_single_info
from service.wmc_service.dv_best50 import b50
from service.wmc_service.dv_bgset import bgset
from service.wmc_service.dv_bind import bind
from service.wmc_service.dv_followlevel_grade import follow_grade


async def wmc(msg_handler,bot,event):
    msgr = str(event.message)
    msg = event.get_plaintext().strip()
    uid = event.user_id
    gid = event.group_id
    mid = event.message_id
    msg_nospace = "".join(msgr.split())

    """

    wmc功能
    查询 单曲信息/单曲别名/单曲封面
    成绩 best50

    """

    if msg.endswith("是什么歌"):
        await get_single_info(uid,msg_handler,event)
        return

    if msg.endswith("有什么别名"):
        await get_alias(uid,msg_handler,event)
        return

    if msg.endswith("的封面"):
        await get_cover(uid,msg_handler,event)
        return


    if msg.startswith("maiset"):
        await bgset(msg_handler,event)
        return

    if msg.startswith("maibind"):
        await bind(msg_handler,event)
        return

    if msg=="b50":
        await b50(uid,msg_handler,event)
        return

    if re.search(r"(.*?)分数列表(.*)", msg):
        await follow_grade(uid,msg_handler,event)
        return
