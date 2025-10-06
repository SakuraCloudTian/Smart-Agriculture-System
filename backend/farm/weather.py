import requests
from bs4 import BeautifulSoup
import re
from lxml import etree
from datetime import datetime
import database
import json



def weather_get():
    url = "http://tianqi.moji.com/"
    cookies = {"moji_setting": "%7B%22internal_id%22%3A663%7D"
               }

    response = requests.get(url, cookies=cookies)

    html_content = response.content

    # 使用BeautifulSoup解析页面内容
    weather_parm = BeautifulSoup(html_content, 'html.parser')
    weather_temp = weather_parm.prettify()
    # 提取连续三天温度
    pattern_temp = r"\d+°\s*/\s*\d+°"
    matches_temp = re.findall(pattern_temp, weather_temp)
    for i in matches_temp:
        today_temp = matches_temp[0]
        tom_temp = matches_temp[1]
        after_temp = matches_temp[2]

    # 提取天气图标
    tree = etree.HTML(weather_temp)
    image_element = tree.xpath("/html/body/div[5]/div[1]/div[1]/ul[1]/li[2]/span/img")
    today_weather_img = image_element[0].get("src")
    image_element = tree.xpath("/html/body/div[5]/div[1]/div[1]/ul[2]/li[2]/span/img")
    tom_weather_img = image_element[0].get("src")
    image_element == tree.xpath("/html/body/div[5]/div[1]/div[1]/ul[3]/li[2]/span/img")
    after_weather_img = image_element[0].get("src")

    # 提取天气元素的文本内容
    element = tree.xpath("/html/body/div[5]/div[1]/div[1]/ul[1]/li[2]/text()")
    today_weather = element[1].strip()
    element = tree.xpath("/html/body/div[5]/div[1]/div[1]/ul[2]/li[2]/text()")
    tom_weather = element[1].strip()
    element = tree.xpath("/html/body/div[5]/div[1]/div[1]/ul[3]/li[2]/text()")
    after_weather = element[1].strip()

    # 提取风的天气
    wind = tree.xpath("/html/body/div[5]/div[1]/div[1]/ul[1]/li[4]/em/text()")
    wind_level = tree.xpath("/html/body/div[5]/div[1]/div[1]/ul[1]/li[4]/b/text()")
    today_wind = wind[0].strip() + wind_level[0].strip()
    wind = tree.xpath("/html/body/div[5]/div[1]/div[1]/ul[2]/li[4]/em/text()")
    wind_level = tree.xpath("/html/body/div[5]/div[1]/div[1]/ul[2]/li[4]/b/text()")
    tom_wind = wind[0].strip() + wind_level[0].strip()
    wind = tree.xpath("/html/body/div[5]/div[1]/div[1]/ul[3]/li[4]/em/text()")
    wind_level = tree.xpath("/html/body/div[5]/div[1]/div[1]/ul[3]/li[4]/b/text()")
    after_wind = wind[0].strip() + wind_level[0].strip()

    # 获取当前温度湿度
    element = tree.xpath("/html/body/div[4]/div[1]/div[2]/em/text()")
    today_temp_now = element[0].strip()
    element = tree.xpath("/html/body/div[4]/div[1]/div[3]/span/text()")
    today_hum = element[0].strip()

    # 获取当前日期
    date_tem = datetime.now().date()
    dates = date_tem.strftime("%Y-%m-%d")

    #获取当前天气的风景图
    image_element = tree.xpath('//div[@id="skin"]')[0]
    background_image  = image_element.get('style')
    pattern = r"url\((.*?)\)"
    match = re.search(pattern, background_image)
    if match:
        today_img = match.group(1)
    else:
        today_img="No image URL found."

    # 存入数据库
    database.insert_data(dates, today_temp, today_temp_now, today_hum, today_weather, today_wind, today_weather_img,
                tom_weather_img, after_weather_img, after_temp, after_wind, after_weather, tom_temp, tom_wind,
                tom_weather,today_img)

