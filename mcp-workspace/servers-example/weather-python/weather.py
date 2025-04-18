import asyncio
import httpx
from mcp.server.fastmcp import FastMCP
from bs4 import BeautifulSoup

# Initialize FastMCP server
mcp = FastMCP("weather")

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

DEFAULT_LOCATION = "昆明"
API_KEY= "a861d0d5e7bf4ee1a83d9a9e4f96d4da"

HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
    )
}

# 天气代码 https://dev.qweather.com/docs/resource/icons/#weather-icons
WEATHER_CODE_MAP = {
    "100": "晴", "101": "多云", "102": "少云", "103": "晴间多云", "104": "阴",
    "150": "晴", "151": "多云", "152": "少云", "153": "晴间多云",
    "300": "阵雨", "301": "强阵雨", "302": "雷阵雨", "303": "强雷阵雨", "304": "雷阵雨伴有冰雹",
    "305": "小雨", "306": "中雨", "307": "大雨", "308": "极端降雨", "309": "毛毛雨/细雨",
    "310": "暴雨", "311": "大暴雨", "312": "特大暴雨", "313": "冻雨", "314": "小到中雨",
    "315": "中到大雨", "316": "大到暴雨", "317": "暴雨到大暴雨", "318": "大暴雨到特大暴雨",
    "350": "阵雨", "351": "强阵雨", "399": "雨",
    "400": "小雪", "401": "中雪", "402": "大雪", "403": "暴雪", "404": "雨夹雪",
    "405": "雨雪天气", "406": "阵雨夹雪", "407": "阵雪", "408": "小到中雪", "409": "中到大雪", "410": "大到暴雪",
    "456": "阵雨夹雪", "457": "阵雪", "499": "雪",
    "500": "薄雾", "501": "雾", "502": "霾", "503": "扬沙", "504": "浮尘",
    "507": "沙尘暴", "508": "强沙尘暴",
    "509": "浓雾", "510": "强浓雾", "511": "中度霾", "512": "重度霾", "513": "严重霾", "514": "大雾", "515": "特强浓雾",
    "900": "热", "901": "冷", "999": "未知"
}

async def fetch_city_info(location, api_key):
    url = f"https://geoapi.qweather.com/v2/city/lookup?key={api_key}&location={location}&lang=zh"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=HEADERS, timeout=30.0)
        response.raise_for_status()
        response = response.json()
    return response.get('location', [])[0] if response.get('location') else None


async def fetch_weather_page(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=HEADERS, timeout=30.0)
        response.raise_for_status()
        response_text = response.text
    return BeautifulSoup(response_text, "html.parser")

def parse_weather_info(soup):
    city_name = soup.select_one("h1.c-submenu__location").get_text(strip=True)

    current_abstract = soup.select_one(".c-city-weather-current .current-abstract")
    current_abstract = current_abstract.get_text(strip=True) if current_abstract else "未知"

    current_basic = {}
    for item in soup.select(".c-city-weather-current .current-basic .current-basic___item"):
        parts = item.get_text(strip=True, separator=" ").split(" ")
        if len(parts) == 2:
            key, value = parts[1], parts[0]
            current_basic[key] = value

    temps_list = []
    for row in soup.select(".city-forecast-tabs__row")[:7]:  # 取前7天的数据
        date = row.select_one(".date-bg .date").get_text(strip=True)
        weather_code = row.select_one(".date-bg .icon")["src"].split("/")[-1].split(".")[0]
        weather = WEATHER_CODE_MAP.get(weather_code, "未知")
        temps = [span.get_text(strip=True) for span in row.select(".tmp-cont .temp")]
        high_temp, low_temp = (temps[0], temps[-1]) if len(temps) >= 2 else (None, None)
        temps_list.append((date, weather, high_temp, low_temp))

    return city_name, current_abstract, current_basic, temps_list

@mcp.tool()
async def get_alerts(location: str, lang: str) -> str:
    """
    获取某个地点的天气，用户应提供一个位置，比如用户说杭州天气，参数为：杭州。
    如果用户说的是省份，默认用省会城市。如果用户说的不是省份或城市而是一个地名，
    默认用该地所在省份的省会城市。

    Args:
        location: 地点名，例如杭州。可选参数，如果不提供则不传
        lang: 返回用户使用的语言code，例如zh_CN/zh_HK/en_US/ja_JP等，默认zh_CN
    """
    api_key = API_KEY
    default_location = DEFAULT_LOCATION
    location = location or default_location

    city_info = await fetch_city_info(location, api_key)
    if not city_info:
        return f"未找到相关的城市: {location}，请确认地点是否正确"

    soup = await fetch_weather_page(city_info['fxLink'])
    if not soup:
        return f"获取天气失败"

    city_name, current_abstract, current_basic, temps_list = parse_weather_info(soup)
    weather_report = f"根据下列数据，用{lang}回应用户的查询天气请求：\n{city_name}未来7天天气:\n"
    for i, (date, weather, high, low) in enumerate(temps_list):
        if high and low:
            weather_report += f"{date}: {low}到{high}, {weather}\n"

    return f"""
    当前天气: {current_abstract}
    当前天气参数: {current_basic}
    (确保只报告指定单日的天气情况，除非未来会出现异常天气；或者用户明确要求想要了解多日天气，如果未指定，默认报告今天的天气。参数为0的值不需要报告给用户，每次都报告体感温度，根据语境选择合适的参数内容告知用户，并对参数给出相应评价)
    """

if __name__ == "__main__":
    # Initialize and run the server
    # mcp.run(transport='stdio')
    result = asyncio.run(get_alerts("昆明", "zh_CN"))
    print(result)