from io import BytesIO

import requests
from PIL import Image
from nonebot.adapters.onebot.v11 import Event, MessageSegment

from core.wmc_core.db_song import multi_output, search_song

from utils.cooldown_decorator import cooldown


@cooldown(10)
async def get_cover(msg_handler, event: Event):
    msg = event.get_plaintext().strip()
    uid=event.get_user_id
    target_songid=msg[:-3]
    song = search_song(target_songid)
    if len(song) != 1:
        selectstr=multi_output(song)
        await msg_handler.finish(selectstr)
    song=song[0]
    try:
        url = f"https://shama.dxrating.net/images/cover/v2/{song['封面']}.jpg"
        resp = requests.get(url, timeout=10,verify=False)
        img = Image.open(BytesIO(resp.content)).convert("RGB")

    except Exception as e:
        print(e)
        img=Image.new("RGB", (160, 160), (200, 200, 200))
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    await msg_handler.finish(MessageSegment.image(buf))