import requests
from datetime import datetime
from flask import Flask, jsonify
import json
from flask_cors import CORS
import database
import weather

app = Flask(__name__)
CORS(app)

#获取近三天天气
@app.route('/api/get_weather', methods=['GET'])
def get_weather():
    response = {
        'message': '查询成功'
    }
    weather.weather_get()
    data = database.get_latest_data()
    return data

#更新二十四小时的气温
@app.route('/api/get_temp', methods=['GET'])
def get_temp():
    with app.app_context():
        url = 'http://tianqi.moji.com/index/getHour24'
        cookies = {"moji_setting": "%7B%22internal_id%22%3A5591%7D"}

        response = requests.get(url, cookies=cookies)

        if response.status_code == 200:
            data = response.json()

            hour24_data = data['hour24']  # 获取hour24字段对应的列表

            filtered_data = []  # 存储提取的数据的二维数组

            for item in hour24_data:
                fpredict_hour = item["Fpredict_hour"]  # 提取Fpredict_hour数据
                ftemp = item["Ftemp"]  # 提取Ftemp数据
                filtered_data.append([fpredict_hour, ftemp])  # 将数据添加到二维数组中
            temp_result = filtered_data[:7]
            # print(filtered_data)
            database.update_temp(temp_result)
            return jsonify({'success': '更新成功'})
        else:
            return jsonify({'error': 'Failed to retrieve weather data'})

#获取24小时的气温
@app.route('/api/tempera_get', methods=['GET'])
def get_temperature():
    # 调用 temp_sel 方法获取温度数据
    temperature_data = database.temp_sel()
    # 返回温度数据
    return temperature_data

#获取前六小时大棚的气温
@app.route('/api/inside_tempera_get', methods=['GET'])
def inside_tempera_get():
    # 调用 temp_sel 方法获取温度数据
    temperature_data = database.inside_temp_sel()
    # 返回温度数据
    return temperature_data

#获取前24小时大棚的湿度
@app.route('/api/moisture_intensity_get', methods=['GET'])
def moisture_intensity():
    # 调用 temp_sel 方法获取温度数据
    mois_and_intensity_data = database.moisture_intensity_get()
    # 返回温度数据
    return mois_and_intensity_data

#获取前24小时大棚的湿度
@app.route('/api/pre_temp_update', methods=['GET'])
def pre_temp_update():
    # 调用 temp_sel 方法获取温度数据
    database.pre_temp_insert()
    # 返回温度数据
    return 200

#获取前24小时大棚的湿度
@app.route('/api/tem_hum_moi_sel', methods=['GET'])
def tem_hum_moi():
    # 调用 temp_sel 方法获取温度数据
    mois_moi_hum_data = database.tem_hum_moi_sel()
    # 返回温度数据
    return mois_moi_hum_data

if __name__ == '__main__':

    app.run()


