from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot,MessageSegment
from datetime import datetime
import random
from core.regular_core.wife_load import MARRIED_FILE, load_json, get_available_users, save_json, DIVORCE_FILE


#每日更新



async def marry(msg_handler,bot: Bot, event: GroupMessageEvent):
    #强匹
    if str(event.message)!='今日老婆':
        return
    gid = str(event.group_id)
    uid = str(event.user_id)
    married = load_json(MARRIED_FILE, {})
    # 已结婚
    if gid in married and uid in married[gid]:
        partner_uid = married[gid][uid]
        try:
            info = await bot.get_group_member_info(group_id=int(gid), user_id=int(partner_uid))
            name = info["card"] or info["nickname"]
        except:
            name = f"用户{partner_uid}"
        await msg_handler.finish(f"💘 你今天已经有老婆啦：\n{name}"+MessageSegment.image(f"https://q1.qlogo.cn/g?b=qq&nk={partner_uid}&s=640"),at_sender=True)

    available = await get_available_users(event.group_id, bot)
    # 抽老婆
    wife_uid = random.choice(available)
    if wife_uid == uid:
        await msg_handler.finish("🎊 今天你的老婆就是你自己！\n水仙.jpg"+MessageSegment.image(f"https://q1.qlogo.cn/g?b=qq&nk={wife_uid}&s=640"), at_sender=True)

    # 保存婚姻
    if gid not in married:
        married[gid] = {}
    married[gid][uid] = wife_uid
    married[gid][wife_uid] = uid
    save_json(MARRIED_FILE, married)

    # 查名字
    try:
        u_info = await bot.get_group_member_info(group_id=int(gid), user_id=int(uid))
        u_name = u_info["card"] or u_info["nickname"]
        w_info = await bot.get_group_member_info(group_id=int(gid), user_id=int(wife_uid))
        w_name = w_info["card"] or w_info["nickname"]
    except:
        u_name = f"用户{uid}"
        w_name = f"用户{wife_uid}"

    await msg_handler.finish(
        f"💞 今日老婆配对成功！\n"
        f"{w_name}({wife_uid})"+MessageSegment.image(f"https://q1.qlogo.cn/g?b=qq&nk={wife_uid}&s=640"),
        at_sender=True
    )

async def divorce(msg_handler,event: GroupMessageEvent):
    #强匹
    if str(event.message)!='离婚':
        return
    gid = str(event.group_id)
    uid = str(event.user_id)
    married = load_json(MARRIED_FILE, {})

    # 没结婚
    if gid not in married or uid not in married[gid]:
        await msg_handler.finish("💔 你还没有结婚哦", at_sender=True)

    # 今日离婚次数限制（每天3次）
    divorce = load_json(DIVORCE_FILE, {})
    today = datetime.now().strftime("%Y-%m-%d")
    key = f"{uid}_{gid}_{today}"
    count = divorce.get(key, 0)

    if count >= 3:
        await msg_handler.finish("⛔ 今天离婚次数已用完（每天最多3次）", at_sender=True)

    # 解除关系
    partner_uid = married[gid][uid]
    del married[gid][uid]
    del married[gid][partner_uid]
    save_json(MARRIED_FILE, married)

    divorce[key] = count + 1
    save_json(DIVORCE_FILE, divorce)

    await msg_handler.finish(f"💔 一段感情的破碎...", at_sender=True)