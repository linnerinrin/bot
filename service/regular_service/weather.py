from config.Expection import WeatherUnlegalError,WeatherRequestError
from core.regular_core.weather_requestweather import get_weather
from utils.cooldown_decorator import cooldown
from utils.error import error_output


@cooldown(30)
async def weather(handler,msg,uid):


        try:
            data=get_weather(msg)
            # JSON解析
            sheng = data["sheng"]
            shi = data["shi"]
            weather1 = data["weather1"]  # 白天天气
            weather2 = data["weather2"]  # 夜间天气
            wd1 = data["wd1"]  # 高温
            wd2 = data["wd2"]  # 低温
            winddirection1 = data["winddirection1"]
            winddirection2 = data["winddirection2"]
            windleve1 = data["windleve1"]
            windleve2 = data["windleve2"]
            now_temp = data["nowinfo"]["temperature"]
            feel_temp = data["nowinfo"]["feelst"]
            humidity = data["nowinfo"]["humidity"]
            uptime = data["uptime"]

            reply = (
                f"🌤 {sheng} {shi} 今日天气\n"
                f"☀ 白天：{weather1}  🌙 夜间：{weather2}\n"
                f"🌡 温度：{wd2}℃ ~ {wd1}℃\n"
                f"🌡 实时：{now_temp}℃  体感：{feel_temp}℃\n"
                f"💧 湿度：{humidity}%\n"
                f"💨 白天风：{winddirection1}{windleve1}\n"
                f"💨 夜间风：{winddirection2}{windleve2}\n"
                f"🕒 更新时间：{uptime}"
            )


            await handler.finish(reply)
        except WeatherUnlegalError:
            await handler.finish("用法错误 正确格式如下\n今日天气 安徽 马鞍山")
        except WeatherRequestError as e:
            await error_output(handler,e)