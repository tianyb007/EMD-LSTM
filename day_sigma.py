# 使用3sigma准则，剔除误差，计算日均值,
# 根据实际计算，这个程序不能去除那些粗大误差啊。
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 读取数据
data_file = "C:/Users/tian/Desktop/data/day_temp_test.txt"

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

    # 计算均值和标准差
    mean_value = np.nanmean(values)
    std_value = np.nanstd(values)

    # 移除异常值（例如，超过3个标准差的观测值）
    for idx, value in enumerate(values):
        if abs(value - mean_value) > 3 * std_value:
            values[idx] = np.nan

    # 计算均值并添加到数据列表
    data.append([pd.to_datetime(date), np.nanmean(values)])

# 将数据转换为DataFrame
df = pd.DataFrame(data, columns=["timestamp", "average_water_temperature"])

# 可视化处理后的数据
plt.figure(figsize=(12, 6))
plt.plot(df["timestamp"], df["average_water_temperature"], linestyle='-')
plt.xlabel("Date")
plt.ylabel("Average Water Temperature")
plt.title("Daily Average Water Temperature - 3sigma")
plt.show()
