from io import BytesIO
from nonebot.adapters.onebot.v11 import MessageSegment

from core.wmc_core.db_song import search_song, multi_output
from core.wmc_core.img_draw import draw_song_card
from utils.cooldown_decorator import cooldown


@cooldown(10)
async def get_single_info(msg_handle, event):
    msg = event.get_plaintext().strip()
    uid = event.user_id
    target_songid = msg[:-4]
    song = search_song(target_songid)
    # 用别名查询有 多个选择
    if len(song) != 1:
        selectstr=multi_output(song)
        await msg_handle.finish(selectstr)

    img = draw_song_card(song[0])
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    await msg_handle.finish(MessageSegment.image(buf))