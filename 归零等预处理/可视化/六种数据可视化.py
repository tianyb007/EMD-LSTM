# 把水温，钻孔面应变和四种分量数据绘制在同一张图片上面。
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# 定义一个函数来读取数据文件并返回数据列表
def read_data_from_file(data_file):
    with open(data_file, "r") as file:
        lines = file.readlines()

    data = []
    for line in lines:
        items = line.split()
        date = items[0]
        values = items[1:]

        for idx, value in enumerate(values):
            values[idx] = float(value)

        data.append([pd.to_datetime(date), np.nanmean(values)])

    return data


# 定义一个函数来对数据进行归一化
def normalize_data(df):
    # 计算非nan值的最小值和最大值
    min_value = df["average_water_temperature"].min(skipna=True)
    max_value = df["average_water_temperature"].max(skipna=True)

    # 定义一个函数，将归一化应用于非nan数据
    def normalize_value(value):
        if pd.isna(value):
            return value
        else:
            return (value - min_value) / (max_value - min_value)

    # 应用归一化函数
    df["average_water_temperature"] = df["average_water_temperature"].apply(normalize_value)

    return df["average_water_temperature"]


# 读取所有数据文件
data_files = [
    # "C:/Users/tian/Desktop/data/water.txt",
    "C:/Users/tian/Desktop/data/zuankong.txt",
    "C:/Users/tian/Desktop/data/EW.txt",
    "C:/Users/tian/Desktop/data/NE.txt",
    "C:/Users/tian/Desktop/data/NS.txt",
    "C:/Users/tian/Desktop/data/NW.txt",
]

# 给每个数据文件分配一个颜色
colors = ["black", "red", "blue", "green", "orange", "purple"]

# 分配数据文件的名称作为图例
labels = ["Temp", "Strain", "EW", "NE", "NS", "NW"]

# 可视化处理后的数据
plt.figure(figsize=(18, 9))

# 读取每个数据文件并将结果绘制到图表上
for i, data_file in enumerate(data_files):

    data = read_data_from_file(data_file)
    df = pd.DataFrame(data, columns=["timestamp", "average_water_temperature"])

    # 对数据进行归一化
    normalized_data = normalize_data(df)

    plt.plot(df["timestamp"], normalized_data, color=colors[i], label=labels[i])
    print(f"Processing {data_file}: {len(normalized_data)} data points")
    print(f"Last 5 data points: {normalized_data[-5:]}")

plt.xlabel("Date")
plt.ylabel("Normalized Daily Average Data")

plt.title("Water Temperature and Borehole Strain Normalized Daily Average Data")
plt.legend(loc="best")  # 添加图例

plt.show()
