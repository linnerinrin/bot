from service.regular_service.bili import bili
from service.regular_service.simple import hello, helpp, fortune, support, choose, eat, drink
from service.regular_service.weather import weather
from service.regular_service.wife import marry, divorce


async def regular(msg_handler,bot,event):
    msgr = str(event.message)
    msg = event.get_plaintext().strip()
    uid = event.user_id
    gid = event.group_id
    mid = event.message_id
    msg_nospace = "".join(msgr.split())


    """
    常规功能 hello/支持/help/运势/b链/天气/配对/选择
    """

    if msg == 'hello':
        await hello(msg_handler)
        return

    if msg == '来支持了':
        await support(uid, msg_handler)
        return

    if msg == 'help':
        await helpp(msg_handler)
        return

    if msg == '我的运势':
        await fortune(msg_handler, uid, mid)
        return

    if 'https:\/\/b23.tv\/' in msg_nospace:
        await bili(msg_handler, msg_nospace)
        return

    if msg.startswith("今日天气"):
        await weather(uid, msg_handler, msg, uid)
        return

    if msg == '今日老婆':
        await marry(msg_handler, bot, event)
        return

    if msg == '离婚':
        await divorce(msg_handler, event)
        return

    if "还是" in msg:
        await choose(msg_handler, msg, mid)
        return

    if "吃什么" in msg:
        await eat(msg_handler, msg, uid)
        return

    if "喝什么" in msg:
        await drink(msg_handler, msg, uid)
        return