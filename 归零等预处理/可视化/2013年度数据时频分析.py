# 原始数据可视化，不进行计算日均值
# 针对玉树地震台的水温观测数据，1分钟采样1次。
# 读取txt文件格式
# 用这个画图，针对单一文件，输出原始数据的可视化图像，对999999和小于9的值进行处理，置为NaN。不对缺失值进行处理。
# 主要处理了2017年的数据

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pywt

# 读取数据
data_file = "C:/Users/tian/Desktop/data/2013_mod.txt"

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

    # 将999999和大于14的值替换为NaN，并将值添加到数据列表
    for idx, value in enumerate(values):
        if float(value) == 999999 or float(value) < 9.86 or float(value) > 9.96:
            value = np.nan
        else:
            value = float(value)
        # 将分钟数据添加到时间戳中
        timestamp = pd.to_datetime(date) + pd.Timedelta(minutes=idx)
        data.append([timestamp, value])

# 将数据转换为DataFrame
df = pd.DataFrame(data, columns=["timestamp", "water_temperature"])

# 按时间戳对数据进行排序
df.sort_values(by=["timestamp"], inplace=True)

# 使用线性插值填充缺失值
df["water_temperature"].interpolate(method="linear", inplace=True)

# 可视化处理后的数据
fig, ax = plt.subplots(figsize=(18, 9))
ax.plot(df["timestamp"], df["water_temperature"], color="black", linewidth=0.5, linestyle="solid")

# 设置x轴日期格式
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
# plt.xticks(rotation=45)
plt.xlabel("Date")
plt.ylabel("Water Temperature")
plt.title("Water Temperature Data 2013")
# plt.grid()
fig.tight_layout()
# 保存图像为 png、jpeg 和 svg 格式
# output_file_base = "C:/Users/tian/Desktop/data/2007-2022"
# plt.savefig(f"{output_file_base}.png", dpi=300)
# plt.savefig(f"{output_file_base}.jpeg", dpi=300)
# plt.savefig(f"{output_file_base}.svg", dpi=300)
# 添加CWT函数和时频图绘制
sampling_period = 1  # 1分钟采样周期
signal = df["water_temperature"].values
time_points = np.arange(len(signal)) * sampling_period

# CWT计算
wavelet = 'cmor1.5-1.0'  # 您可以尝试其他小波如 'morl', 'cgau5' 等
scales = np.arange(1, 101)  # 调整scales范围以获得更精细或更粗糙的时频表示
cwt_coefficients, frequencies = pywt.cwt(signal, scales, wavelet, sampling_period)

# 时频图绘制
fig, ax = plt.subplots(figsize=(18, 9))
cwt_im = ax.imshow(np.abs(cwt_coefficients), cmap='viridis', aspect='auto', extent=[0, len(signal), 1, max(scales)])
plt.xlabel("Time (minutes)")
plt.ylabel("Scale")
plt.title("CWT Time-Frequency Representation")
plt.colorbar(cwt_im, label="Magnitude")
fig.tight_layout()
plt.show()

# 保存处理过的数据到CSV文件
# output_file = "C:/Users/tian/Desktop/data/processed_data.csv"
# df.to_csv(output_file, index=False)
