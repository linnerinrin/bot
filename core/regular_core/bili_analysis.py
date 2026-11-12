import re
import aiohttp

from config.Expection import BiliRequestError


async def bili_analysis(msg):
    match = re.search(r'"qqdocurl":"(.*?)"', msg)
    if not match:
        return None, None

    url_match = match.group(1)
    url_match = url_match.replace("\\/", "/")
    short_url = url_match.replace("&amp;", "&")

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    timeout = aiohttp.ClientTimeout(total=10)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.head(short_url, headers=headers, allow_redirects=True) as resp:
            final_url = str(resp.url)

        bv_match = re.search(r"BV[A-Za-z0-9]{10}", final_url)
        if not bv_match:
            return None, None
        bvid = bv_match.group()

        api = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
        async with session.get(api, headers=headers) as resp:
            data = await resp.json()

    if data.get("code") != 0:
        raise BiliRequestError

    info = data["data"]
    return bvid, info
