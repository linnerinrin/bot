import re
from io import BytesIO

from nonebot.adapters.onebot.v11 import MessageSegment

from core.wmc_core.resimg_level import paste_level
from utils.cooldown_decorator import cooldown


@cooldown(30)
async def follow_grade(msg_handler,event):
    #正则匹配到关键词 提取key和index
    msg = event.get_plaintext().strip()
    match = re.search(r"(.*?)分数列表(.*)", msg)
    key=None
    index=None
    try:
        key=match[1]
        index=match[2]
    except:
        await msg_handler.finish("请检查指令是否正确 如 13+分数列表2")

    uid = event.user_id
    await msg_handler.send("正在绘制中...")

    for seg in event.message:
        if seg.type == "at":
            uid = seg.data.get("qq")
            if uid == "all":
                return
    #根据编码判断输出字符串还是图像
    try:
        cde,img=paste_level(uid,key,index)
        if cde==1:
            img=img.convert("RGB")
            buf = BytesIO()
            img.save(buf, format="JPEG")
            buf.seek(0)
            await msg_handler.finish(MessageSegment.image(buf))
        if cde==2:
            await msg_handler.finish(img)
    except KeyError as e:
        print(e)
        await msg_handler.finish("该账号未绑定水鱼查分器")