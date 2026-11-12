import json
import os
from datetime import datetime
from nonebot.adapters.onebot.v11 import Bot
from config.regular_setting import regular_settings

DATA_DIR = regular_settings.Wife_local
os.makedirs(DATA_DIR, exist_ok=True)
MARRIED_FILE = os.path.join(DATA_DIR, "married.json")
DIVORCE_FILE = os.path.join(DATA_DIR, "divorce_count.json")


def check_reset():
    today = datetime.now().strftime("%Y-%m-%d")
    last = load_json(os.path.join(DATA_DIR, "last_day.txt"), "")
    #如果记录日期不是今天 文件清空
    if last != today:
        save_json(MARRIED_FILE, {})
        save_json(DIVORCE_FILE, {})
        save_json(os.path.join(DATA_DIR, "last_day.txt"), today)

# 读取/保存数据
def load_json(path, default):
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(default, f, ensure_ascii=False, indent=2)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

#获取可抽取用户
async def get_available_users(group_id: int, bot: Bot):
    check_reset() #先更新
    married = load_json(MARRIED_FILE, {})
    group = str(group_id)
    available = []
    #获取列表
    try:
        member_list = await bot.get_group_member_list(group_id=group_id)
    except:
        return available
    #如果结婚了直接滚
    for member in member_list:
        uid_str = str(member["user_id"])
        if group in married and uid_str in married[group]:
            continue
        available.append(uid_str)
    return available