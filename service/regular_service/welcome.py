from nonebot import on_notice
from nonebot.adapters.onebot.v11 import (
    GroupIncreaseNoticeEvent,
    GroupDecreaseNoticeEvent,
    Bot
)

# 入群欢迎
welcome = on_notice(priority=10,block=False)

@welcome.handle()
async def _(bot: Bot, event: GroupIncreaseNoticeEvent):
    user_id = event.get_user_id()
    if user_id==bot.self_id:
        return
    group_id = event.group_id

    # 获取群成员信息
    info = await bot.get_group_member_info(group_id=group_id, user_id=int(user_id))
    nickname = info.get("card") or info.get("nickname")

    await welcome.finish(f"✨ 欢迎 {nickname}({user_id}) 加入本群！")

# 退群提示
leave = on_notice(priority=10)

@leave.handle()
async def _( event: GroupDecreaseNoticeEvent):
    user_id = event.get_user_id()
    await leave.finish(f"👋 {user_id} 永远地离开了我们")