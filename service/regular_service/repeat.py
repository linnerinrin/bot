import re
from nonebot.adapters.onebot.v11 import GroupMessageEvent,MessageSegment,Message

from core.regular_core.repeat_cooldown import check_cd
from core.regular_core.repeat_get_cq_url import get_url_from_cq

last_msg = {}
repeat_count = {}

async def repeatf(msg_handler,event: GroupMessageEvent):
    isface=False
    group = event.group_id
    msgr = str(event.message).strip()
    if msgr.startswith("[CQ:image,summary=&#91;动画表情&#93;"):
        isface=True
        url=get_url_from_cq(msgr,r'url=([^,]+)')
        msg=get_url_from_cq(msgr,r'file=([^.]+)\.')
    else:
        msg=msgr
    if group not in last_msg:
        last_msg[group] = ""
        repeat_count[group] = 0

    if msg == last_msg[group]:
        repeat_count[group] += 1
    else:
        last_msg[group] = msg
        repeat_count[group] = 0

    if repeat_count[group] >= 1:
        ok=check_cd(group,60)
        if ok:
            if isface:
                await msg_handler.finish(MessageSegment.image(url))
            else:
                await msg_handler.finish(Message(msg))