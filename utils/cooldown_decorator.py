import time
import os

def cooldown(cd_seconds,tip=True):
    cd_dict = {}
    tip_flag = True

    def decorator(func):
        async def wrapper(uid,handler,*args,**kwargs):
            nonlocal tip_flag
            now = time.time()
            if uid not in cd_dict:
                cd_dict[uid] = 0

            if cd_dict[uid] > now:
                if tip_flag and tip:
                    tip_flag = False
                    await handler.finish(f"太急啦，{int(cd_dict[uid]-now)}秒后再试试吧~")
                return

            cd_dict[uid] = now + cd_seconds
            tip_flag = True
            await func(handler,*args,**kwargs)

        return wrapper
    return decorator