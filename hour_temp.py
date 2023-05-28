# 计算了小时均值，看着还不错，先留着

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

# 读取数据
data_file = "C:/Users/tian/Desktop/data/2007.txt"

# 从txt文件中读取数据并转换为列表
with open(data_file, "r") as file:
    lines = file.readlines()

# 初始化空的数据列表
data = []

# 处理每一行数据
for line in lines:
    items = line.split()
    date = items[0]
    values = items[1:]

    # 将999999替换为NaN
    for idx, value in enumerate(values):
        if float(value) == 999999 or float(value) > 13:
            values[idx] = np.nan
        else:
            values[idx] = float(value)

    # 计算每小时的均值
    hourly_values = [np.nanmean(values[i:i + 60]) for i in range(0, len(values), 60)]

    # 添加到数据列表
    for i, hourly_value in enumerate(hourly_values):
        data.append([pd.to_datetime(date) + pd.Timedelta(hours=i), hourly_value])

# 将数据转换为DataFrame
df = pd.DataFrame(data, columns=["timestamp", "average_water_temperature"])

# 可视化处理后的数据
plt.figure(figsize=(12, 6))
plt.plot(df["timestamp"], df["average_water_temperature"], linestyle='-', color="black", linewidth=1)
plt.xlabel("Date")
plt.ylabel("Hourly Average Water Temperature")
plt.title("Hourly Average Water Temperature")
plt.show()
