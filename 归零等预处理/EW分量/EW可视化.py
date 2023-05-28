# 对钻孔原始数据文件进行可视化，进行日均值的计算。
# 这个方法是有效的，可以展示正常的数据了，之前不正常的原因是有些数据因为仪器的故障，导致测量的值偏大。
# 计算了日均值，显示的日均值的曲线还不错。


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 读取数据
# data_file = "C:/Users/tian/Desktop/data/day_temp_test.txt"
data_file = "C:/Users/tian/Desktop/data/fenliang/EW_adjusted_4.txt"
# data_file = "C:/Users/tian/Desktop/data/fenliang/NS.txt"
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
        if float(value) == 999999 or float(value) > 300000:
            values[idx] = np.nan
        else:
            values[idx] = float(value)

    # 计算均值并添加到数据列表
    data.append([pd.to_datetime(date), np.nanmean(values)])

# 将数据转换为DataFrame
df = pd.DataFrame(data, columns=["timestamp", "average_strain"])

# 可视化处理后的数据
plt.figure(figsize=(18, 9))
plt.plot(df["timestamp"], df["average_strain"], color="black")

plt.xlabel("Date")
plt.ylabel("Average Strain")
# fig.tight_layout()
plt.title("Daily Average Strain EW")
plt.show()

