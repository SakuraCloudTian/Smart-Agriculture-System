import mysql.connector
import re
import random
from datetime import datetime
import json
import weather

dates = ""
today_temp = ""
today_temp_now = ""
today_hum = ""
today_weather = ""
today_wind = ""
today_weather_img = ""
tom_weather_img = ""
after_weather_img = ""
after_temp = ""
after_wind = ""
after_weather = ""
tom_temp = ""
tom_wind = ""
tom_weather = ""
today_img=""
#插入更新之后的天气
def insert_data(dates, today_temp, today_temp_now, today_hum, today_weather, today_wind, today_weather_img,
                tom_weather_img, after_weather_img, after_temp, after_wind, after_weather, tom_temp, tom_wind,
                tom_weather,today_img):
    # 建立数据库连接
    conn = mysql.connector.connect(
        host="124.222.244.117",
        user="swu4",
        password="swu4",
        database="swu4"
    )

    # 创建一个游标对象
    cursor = conn.cursor()

    # 插入数据
    # 使用参数化查询构建 SQL 语句
    sql = "INSERT INTO weather (date, today_temp,today_temp_now,today_hum,today_weather,today_wind,today_weather_img,after_temp,after_wind,after_weather,tom_temp,tom_wind,tom_weather,tom_weather_img,after_weather_img,today_img) VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s,%s, %s, %s)"
    values = (
    dates, today_temp, today_temp_now, today_hum, today_weather, today_wind, today_weather_img, after_temp, after_wind,
    after_weather, tom_temp, tom_wind, tom_weather, tom_weather_img, after_weather_img,today_img)
    # 执行 SQL 语句
    cursor.execute(sql, values)

    # 提交事务
    conn.commit()

    # 关闭游标和连接
    cursor.close()
    conn.close()

#获取最新的天气信息
def get_latest_data():
    weather.weather_get()
    # 建立数据库连接
    conn = mysql.connector.connect(
        host="124.222.244.117",
        user="swu4",
        password="swu4",
        database="swu4"
    )

    # 创建一个游标对象
    cursor = conn.cursor()

    # 执行MQL查询
    query = "SELECT * FROM weather ORDER BY date DESC LIMIT 1"
    cursor.execute(query)

    # 获取查询结果
    result = cursor.fetchone()
    # # 将查询结果转换为 JSON 字符串
    # json_data = json.dumps(result)
    data_json = []
    # # 将 JSON 字符串赋值给变量 data
    # data = json_data
    # 将结果转换为字典格式
    columns = [col[0] for col in cursor.description]
    data = dict(zip(columns, result))
    data_json.append(data)
    # 关闭游标和连接
    cursor.close()
    conn.close()
    return data_json

#更新外界未来24h温度信息
def update_temp(temp_result):
    # 建立数据库连接
    conn = mysql.connector.connect(
        host="124.222.244.117",
        user="swu4",
        password="swu4",
        database="swu4"
    )

    # 创建一个游标对象
    cursor = conn.cursor()

    try:
        for row in temp_result:
            time_id = row[0]
            temp = row[1]

            # 更新数据
            sql = "UPDATE today_temp SET temp = %s WHERE time_id = %s"
            values = (temp, time_id)
            cursor.execute(sql, values)

        # 提交事务
        conn.commit()
        print("数据更新成功")

    except mysql.connector.Error as error:
        # 发生错误时回滚事务
        conn.rollback()
        print("数据更新失败:", error)

    finally:
        # 关闭游标和连接
        cursor.close()
        conn.close()

#查询前后六小时外界气温和大棚内预测温度
def temp_sel():
    # pre_temp_insert()
    # 获取当前小时
    current_time = datetime.now()
    current_hour = current_time.hour
    # 计算前六个小时和后六个小时的时间范围
    start_time = (current_hour - 6) % 24
    end_time = (current_hour + 6) % 24
    counter_temp()

    # 建立数据库连接
    conn = mysql.connector.connect(
        host="124.222.244.117",
        user="swu4",
        password="swu4",
        database="swu4"
    )
    # 创建一个游标对象
    cursor = conn.cursor()
    # 查询数据库中的数据
    # 使用 SQL 语句查询，根据使用的数据库和库的方法进行修改
    if (current_hour >= 18):
        query = f"SELECT * FROM today_temp WHERE (time_id >= {start_time} AND time_id <= {current_hour}) OR ((time_id >= {current_hour} OR time_id <= {end_time}))"
    if (current_hour < 6):
        query = f"SELECT * FROM today_temp WHERE (time_id >= {start_time} OR time_id <= {current_hour}) OR ((time_id >= {current_hour} AND time_id <= {end_time}))"
    if (current_hour >= 6 and current_hour < 18):
        query = f"SELECT * FROM today_temp WHERE time_id >= {start_time} AND time_id <= {end_time}"

    cursor.execute(query)

    # 获取查询结果并转化成json格式
    result = cursor.fetchall()
    json_data = []
    for item in result:
        time_id = item[0]
        temperature = item[1]
        pre_temperature=item[3]
        json_item = {"time": time_id, "temp": temperature,"pre_temp":pre_temperature}
        json_data.append(json_item)

    json_str = json.dumps(json_data)

    # 返回查询结果
    return json_str

#查询前六小时大棚内温度
def inside_temp_sel():
    # 创建与数据库的连接
    conn = mysql.connector.connect(
        host="124.222.244.117",
        user="swu4",
        password="swu4",
        database="swu4"
    )
    # 获取当前小时
    current_time = datetime.now()
    current_hour = current_time.hour
    # 计算前六个小时的时间范围
    start_time = (current_hour - 6) % 24
    # pre_temp_insert()
    # 创建一个游标对象
    cursor = conn.cursor()

    if (current_hour < 6):
        query = f"SELECT * FROM today_temp WHERE (time_id >= {start_time} OR time_id <= {current_hour})"
    if (current_hour >= 6):
        query = f"SELECT * FROM today_temp WHERE time_id >= {start_time} AND time_id <= {current_hour}"

    # 查询数据库中的数据
    cursor.execute(query)

    # 获取查询结果
    result = cursor.fetchall()
    json_data = []
    for item in result:
        time_id = item[0]
        inside_temperature = item[2]

        json_item = {"time": time_id, "inside_temp": inside_temperature}
        json_data.append(json_item)

    json_str = json.dumps(json_data)

    # 关闭游标和数据库连接
    cursor.close()
    conn.close()

    return json_str


def counter_temp():
    # 创建与数据库的连接
    conn = mysql.connector.connect(
        host="124.222.244.117",
        user="swu4",
        password="swu4",
        database="swu4"
    )
    # 创建一个游标对象
    cursor = conn.cursor()
    # 查询数据库中的数据
    query = "SELECT * FROM today_temp ORDER BY time_id"
    cursor.execute(query)
    # 获取查询结果
    result = cursor.fetchall()
    data = []
    # 循环遍历原始数据，逐行存入四维数组
    for row in result:
        temp_row = []
        for item in row:
            temp_row.append(item)
        data.append(temp_row)

    for i in range(len(data) - 1):
        current_item = data[i][1]
        next_item = data[i + 1][1]
        if (current_item - next_item)==1:
            data[i+1][3]=data[i][2]+random.randint(0, 2)
        elif (current_item - next_item)>1:
            data[i+1][3]=data[i][2]+random.randint(0, 3)
        elif (current_item - next_item)==-1:
            data[i+1][3]=data[i][2]-random.randint(0, 2)
        elif (current_item - next_item)<-1:
            data[i+1][3]=data[i][2]-random.randint(0, 3)
        elif (current_item - next_item)==0:
            data[i+1][3] =data[i][2]+random.randint(0,1)
        if(i==0):
            data[i][3]=data[i][2]+random.randrange(-1, 2)
    # 关闭游标和数据库连接
    cursor.close()
    conn.close()
    return data

def pre_temp_insert():
    try:
        data=counter_temp()
        # 建立数据库连接
        connection = mysql.connector.connect(
            host="124.222.244.117",
            user="swu4",
            password="swu4",
            database="swu4"
        )
        # 获取当前小时
        current_time = datetime.now()
        current_hour = current_time.hour
        # 计算后六个小时的时间范围
        end_time = (current_hour + 6) % 24
        # 创建游标对象
        cursor = connection.cursor()
        for i in range(len(data)):
            if (i>=current_hour and i<=end_time):
                sql = "UPDATE today_temp SET pre_temp = %s WHERE time_id = %s"
                values = (data[i][3], i)
                cursor.execute(sql, values)
            if(current_hour>end_time and (i>=current_hour or i<=end_time)):
                sql = "UPDATE today_temp SET pre_temp = %s WHERE time_id = %s"
                values = (data[i][3], i)
                cursor.execute(sql, values)

        # 提交事务
        connection.commit()

        print("预测温度插入成功")

    except mysql.connector.Error as error:
        print("预测温度插入失败:", error)

    finally:
        # 关闭游标和数据库连接
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def moisture_intensity_get():
    # 创建与数据库的连接
    conn = mysql.connector.connect(
        host="124.222.244.117",
        user="swu4",
        password="swu4",
        database="swu4"
    )
    # 获取当前小时
    current_time = datetime.now()
    current_hour = current_time.hour
    # 计算前六个小时的时间范围
    start_time = (current_hour - 6) % 24
    # pre_temp_insert()
    # 创建一个游标对象
    cursor = conn.cursor()

    query = f"SELECT * FROM today_temp WHERE time_id >= 0"

    # 查询数据库中的数据
    cursor.execute(query)

    # 获取查询结果
    result = cursor.fetchall()
    json_data = []
    for item in result:
        time_id = item[0]
        moisture = item[4]
        intensity=item[5]
        hum=item[6]
        json_item = {"time": time_id, "moisture": moisture,"intensity":intensity,"hum":hum}
        json_data.append(json_item)

    json_str = json.dumps(json_data)

    # 关闭游标和数据库连接
    cursor.close()
    conn.close()

    return json_str

#查询前六小时大棚内温度、湿度、土壤湿度
def tem_hum_moi_sel():
    # 创建与数据库的连接
    conn = mysql.connector.connect(
        host="124.222.244.117",
        user="swu4",
        password="swu4",
        database="swu4"
    )
    # 获取当前小时
    current_time = datetime.now()
    current_hour = current_time.hour
    # 计算前六个小时的时间范围
    start_time = (current_hour - 6) % 24
    # pre_temp_insert()
    # 创建一个游标对象
    cursor = conn.cursor()

    if (current_hour < 6):
        query = f"SELECT * FROM today_temp WHERE (time_id >= {start_time} OR time_id <= {current_hour})"
    if (current_hour >= 6):
        query = f"SELECT * FROM today_temp WHERE time_id >= {start_time} AND time_id <= {current_hour}"

    # 查询数据库中的数据
    cursor.execute(query)

    # 获取查询结果
    result = cursor.fetchall()
    json_data_temp = []
    for item in result:
        time_id = item[0]
        inside_temperature = item[2]
        json_item_temp = {"time": time_id, "inside_temp": inside_temperature,"temp":"温度"}
        json_data_temp.append(json_item_temp)
    json_data_moi = []
    for item in result:
        time_id = item[0]
        inside_moi = item[4]
        json_item_moi = {"time": time_id, "moisture": inside_moi,"moi":"土壤湿度"}
        json_data_moi.append(json_item_moi)
    json_data_hum = []
    for item in result:
        time_id = item[0]
        inside_hum = item[6]
        json_item_hum = {"time": time_id, "hummity": inside_hum,"hum":"空气湿度"}
        json_data_hum.append(json_item_hum)
    # print(json_data_temp,json_data_moi,json_data_hum)
    json_str = json.dumps(json_data_temp+json_data_moi+json_data_hum)
    # 关闭游标和数据库连接
    cursor.close()
    conn.close()

    return json_str