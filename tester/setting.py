"""

用于玩家绑定token以及设置输出成绩图的偏好的函数集合

bind 绑定用户的水鱼查分器token
bgset 个性化用户成绩图

"""
import json
from .utils import search_song, multi_output, get_abs_path
from .records import get_full_grade

empty_dict={"token": None, "bg": None, "plate": None}

command2index={
    "背景":"bg",
    "牌子":"plate",
}

def info_load():
    with open(rf"{get_abs_path()}/data/wmc/datasets/userinfo.json", "r", encoding="utf-8") as f:
        user_info = json.load(f)
    return user_info

def info_dump(user_info,uid,cmd,tid):
    if str(uid) not in user_info: user_info[str(uid)] = empty_dict
    user_info[str(uid)][cmd] = tid
    with open(rf"{get_abs_path()}/data/wmc/datasets/userinfo.json", "w", encoding="utf-8") as f:
        json.dump(user_info, f, ensure_ascii=False, indent=2)

#绑定用户在水鱼查分器的token 用于查询具体成绩
async def bind(handler,event):
    user_info=info_load()
    uid=event.user_id
    msg = event.get_plaintext().strip()
    try:
        token=msg.split(" ")[1]
        valid=get_full_grade(token)["records"]
    except Exception as e:
        await handler.finish("Token不存在或失效或未输入正确指令\n请尝试登录水鱼查分网站 https://maimai.diving-fish.com/ 注册账号，并跟随使用指南完成账号注册及成绩导入\n随后在“编辑个人资料”页面中选择“成绩导入Token”并复制有效Token\n切记！绑定水鱼Token后记得及时撤回Token！")
        return
    info_dump(user_info,uid,"token",token)
    await handler.finish("绑定成功！请及时撤回Token！")

#用于设置玩家的成绩图背景 maiset 背景 ...
async def bgset(handler,event):
    user_info=info_load()
    uid=event.user_id
    msg = event.get_plaintext().strip()
    try:
        cmd=command2index[msg.split(" ")[1]]
        tid=msg.split(" ")[2]
        if cmd=="bg":
            target=search_song(tid)
            if len(target)!=1:
                await handler.finish(multi_output(target))
                return
            else:
                tid=target[0]["索引"]
    except Exception as e:
        print(e)
        await handler.finish(
            "请确保设置指令正确\n可供选择的指令有\nmaiset 背景 [乐曲id/标题/别名]\nmaiset 牌子 [收藏品id]")
    info_dump(user_info,uid,cmd,tid)
    await handler.finish("设置成功！")





