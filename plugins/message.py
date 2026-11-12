from nonebot import on_message
from handler.regular_handler import regular
from handler.wmc_handler import wmc
from plugins.fliter import fliter_group
from service.regular_service.repeat import repeatf
msg_handler=on_message(block=False)
@msg_handler.handle()
async def _(bot,event):
    is_fliter=fliter_group(event.group_id)
    if not is_fliter:
        return
    await regular(msg_handler,bot,event)
    await wmc(msg_handler,bot,event)
    await repeatf(msg_handler,event)
    return


