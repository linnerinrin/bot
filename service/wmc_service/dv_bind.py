from core.wmc_core.db_infocr import info_load, info_dump
from core.wmc_core.dv_records import get_full_grade


async def bind(handler, event):
    user_info = info_load()
    uid = event.user_id
    msg = event.get_plaintext().strip()
    try:
        token = msg.split(" ")[1]
        get_full_grade(token)["records"]
    except Exception as e:
        await handler.finish("Token不存在或失效或未输入正确指令\n请尝试登录水鱼查分网站 https://maimai.diving-fish.com/ 注册账号，并跟随使用指南完成账号注册及成绩导入\n随后在“编辑个人资料”页面中选择“成绩导入Token”并复制有效Token\n切记！绑定水鱼Token后记得及时撤回Token！")
        return
    info_dump(user_info, uid, "token", token)
    await handler.finish("绑定成功！请及时撤回Token！")
