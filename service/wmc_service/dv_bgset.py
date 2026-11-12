from core.wmc_core.db_infocr import info_load, info_dump
from core.wmc_core.db_song import search_song, multi_output

command2index = {"背景": "bg", "牌子": "plate"}


async def bgset(handler, event):
    user_info = info_load()
    uid = event.user_id
    msg = event.get_plaintext().strip()
    try:
        cmd = command2index[msg.split(" ")[1]]
        tid = msg.split(" ")[2]
        if cmd == "bg":
            target = search_song(tid)
            if len(target) != 1:
                await handler.finish(multi_output(target))
                return
            else:
                tid = target[0]["索引"]
    except Exception as e:
        print(e)
        await handler.finish("请确保设置指令正确\n可供选择的指令有\nmaiset 背景 [乐曲id/标题/别名]\nmaiset 牌子 [收藏品id]")
    info_dump(user_info, uid, cmd, tid)
    await handler.finish("设置成功！")
