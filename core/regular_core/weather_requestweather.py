import requests

from config.Expection import WeatherUnlegalError, WeatherRequestError
from config.regular_setting import regular_settings

API_URL = regular_settings.WEATHERAPI_URL
API_KEY = regular_settings.WEATHERAPI_KEY
API_ID = regular_settings.WEATHERAPI_ID
def get_weather(msg):

    parts = msg.split()
    if len(parts) < 3 or not parts[1].strip() or not parts[2].strip():
        raise WeatherUnlegalError

    city1 = parts[1].strip()
    city2 = parts[2].strip()
    params = {
            "key": API_KEY,
            "id": API_ID,
            "sheng": city1,
            "place": city2,
        }
    # 发起请求
    resp = requests.get(API_URL, params=params, timeout=10)
    data = resp.json()
    if data.get("code") != 200:
        raise WeatherRequestError

    return data