from io import BytesIO

from nonebot.adapters.onebot.v11 import MessageSegment
from config.Expection import DivingFishRequestError, NoRescourseError, LXNSRequestError, QLogoRequestError
from core.wmc_core.resimg_best50 import paste_b50
from utils.cooldown_decorator import cooldown
from utils.error import error_output


@cooldown(30)
async def b50(msg_handler,event):
    msg = event.get_plaintext().strip()
    uid = event.user_id
    await msg_handler.send("正在绘制中...")

    for seg in event.message:
        if seg.type == "at":
            uid = seg.data.get("qq")
            if uid == "all":
                return
    try:
        img=paste_b50(uid).convert("RGB")
        buf = BytesIO()
        img.save(buf, format="JPEG")
        buf.seek(0)
        await msg_handler.finish(MessageSegment.image(buf))
    except KeyError:await msg_handler.finish("该账号未绑定水鱼查分器")
    except DivingFishRequestError as e:await error_output(msg_handler,e)
    except NoRescourseError as e:await error_output(msg_handler, e)
    except LXNSRequestError as e:await error_output(msg_handler, e)
    except QLogoRequestError as e:await error_output(msg_handler, e)
