from nonebot.adapters.onebot.v11 import MessageSegment
import random
from datetime import date
from config.regular_setting import regular_settings
from utils.cooldown_decorator import cooldown

fortune_msgs = regular_settings.FORTUNE_LIST
events = regular_settings.FORTUNE_EVENT_LIST
eats=regular_settings.EAT_LIST
drinks=regular_settings.DRINK_LIST

async def hello(handler):
    await handler.finish("你好呀")

@cooldown(15)
async def support(handler):
    await handler.finish(MessageSegment.image(regular_settings.QRcode_local))

async def helpp(handler):
    await handler.finish(regular_settings.HELP_LIST)

async def fortune(handler,user_id,message_id):
    today = str(date.today())
    seed = hash(f"{user_id}_{today}")
    rng = random.Random(seed)


    score = rng.randint(0, 100)
    # 匹配评语
    comment = ""
    for low, high, text in fortune_msgs:
        if low <= score <= high:
            comment = text
            break

    event_num = rng.randint(6, 10)
    # 随机选不重复事件
    selected = rng.sample(events, min(event_num, len(events)))

    res = [
        "🔮 今日运势",
        f"总分：{score}/100 {comment}",
        "——————————"
    ]

    for thing in selected:
        choice = rng.choice(["宜", "忌"])
        res.append(f"{choice} 【{thing}】")

    final = "\n".join(res)

    await handler.finish(
        MessageSegment.reply(message_id) +  # 回复原消息
        MessageSegment.at(user_id) +  # @对方
        "\n" + final  # 运势内容
    )

async def choose(handler,msg,mid):
    options = msg.split("还是")
    options = [opt.strip() for opt in options if opt.strip()]
    # 选项长度大于10不计入命令
    for option in options:
        if len(option) > 10:
            return
    result = random.choice(options)
    await handler.finish(MessageSegment.reply(mid) + f"{result}")

async def eat(handler,msg,uid):
    if "吃什么" in msg:
        subj = msg.split("吃什么")[0]
        if not subj:
            subj="您"
        today = str(date.today())
        seed = hash(f"{uid}_{today}_{subj}")
        rng = random.Random(seed)
        res=rng.choice(eats)
        await handler.finish(f"Rei建议{subj}吃{res}！")

async def drink(handler,msg,uid):
    if "喝什么" in msg:
        subj = msg.split("喝什么")[0]
        if not subj:
            subj="您"
        today = str(date.today())
        seed = hash(f"{uid}_{today}_{subj}")
        rng = random.Random(seed)
        res=rng.choice(drinks)
        await handler.finish(f"Rei建议{subj}喝{res}！")



