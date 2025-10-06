import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
import numpy as np

# 加载数据
data = pd.read_csv('data.csv')

# 将"time"列转换为日期时间格式
data['time'] = pd.to_datetime(data['time'])

# 将"time"列设为索引
data.set_index('time', inplace=True)

# 明确指定数据的频率
data.index.freq = '15T'  # 调整'15T'以符合你的实际数据

# 检查数据中是否存在缺失值
print(data.isnull().sum())

# 如果存在缺失值，可以使用插值方法填充
data.interpolate(method='time', inplace=True)

# 用于存放预测结果的字典
forecasts = {}

# 对每个列进行预测
for column in data.columns:
    if column != 'time':
        # 使用 "column" 列的中位数填充空值
        median = data[column][int(len(data)/2):].median()
        data[column].fillna(median, inplace=True)

        # 绘制图表
        data[column].plot(figsize=(15, 10))
        plt.show()

        # 使用ARIMA模型进行预测
        model = ARIMA(data[column], order=(5,1,0))
        model_fit = model.fit()

        # 进行预测
        forecast = model_fit.forecast(steps=10)

        # 保存预测结果
        forecasts[column] = forecast

        # 打印预测结果
        print(f'Forecast for {column}: ', forecast)

# 可视化所有预测结果
for column, forecast in forecasts.items():
    plt.figure(figsize=(10,6))
    plt.plot(forecast, label=f'Forecast for {column}')
    plt.legend()
    plt.show()

# 将预测结果转化为数据框
forecast_df = pd.DataFrame(forecasts)

# 计算预测时间序列的索引
forecast_index = pd.date_range(start=data.index[-1], periods=11, freq='15T')[1:]
forecast_df.set_index(forecast_index, inplace=True)

# 保存预测结果为CSV文件
forecast_df.to_csv('forecast.csv')
