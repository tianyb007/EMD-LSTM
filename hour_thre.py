# 计算均值，先留着

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

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
        if float(value) == 999999:
            values[idx] = np.nan
        else:
            values[idx] = float(value)

    # 计算Z-score
    z_scores = np.abs(stats.zscore(values, nan_policy='omit'))

    # 移除异常值（例如，Z-score大于2的观测值）
    threshold = 0.5
    for idx, (value, z_score) in enumerate(zip(values, z_scores)):
        if z_score > threshold:
            values[idx] = np.nan

    # 计算均值并添加到数据列表
    data.append([pd.to_datetime(date), np.nanmean(values)])

# 将数据转换为DataFrame
df = pd.DataFrame(data, columns=["timestamp", "average_water_temperature"])

# 可视化处理后的数据
plt.figure(figsize=(12, 6))
plt.plot(df["timestamp"], df["average_water_temperature"], linestyle='-', color="black", linewidth=1)
plt.xlabel("Date")
plt.ylabel("Average Water Temperature")
plt.title("Daily Average Water Temperature")
plt.show()
