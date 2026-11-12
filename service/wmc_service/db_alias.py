from nonebot.adapters.onebot.v11 import Event

from core.wmc_core.db_song import search_song, multi_output
from utils.cooldown_decorator import cooldown


@cooldown(10)
async def get_alias(msg_handler,event:Event):
    msg = event.get_plaintext().strip()
    uid = event.user_id
    target_songid=msg[:-5]
    song = search_song(target_songid)

    if len(song) != 1:
        selectstr = multi_output(song)
        await msg_handler.finish(selectstr)
    song = song[0]
    await msg_handler.finish(song["曲名"]+"有如下别名\n"+song["别名"])