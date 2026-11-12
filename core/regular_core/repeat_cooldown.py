import time
from collections import defaultdict

cd=defaultdict(float)
def check_cd(user_id,cd_seconds):
    now = time.time()
    if cd[user_id] > now:
        return False
    cd[user_id] = now + cd_seconds
    return True