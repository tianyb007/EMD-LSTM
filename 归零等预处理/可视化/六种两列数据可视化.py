import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 定义一个函数来读取数据文件并返回数据列表
def read_data_from_file(data_file):
    df = pd.read_csv(data_file, sep=" ", header=None, names=["timestamp", "value"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], format="%Y%m%d%H%M")

    # 计算日均值
    df = df.resample("D", on="timestamp").mean().reset_index()

    return df

# 定义一个函数来对数据进行归一化
def normalize_data(df):
    min_value = df["value"].min(skipna=True)
    max_value = df["value"].max(skipna=True)

    def normalize_value(value):
        if pd.isna(value):
            return value
        else:
            return (value - min_value) / (max_value - min_value)

    df["value"] = df["value"].apply(normalize_value)
    return df["value"]

# 读取所有数据文件
data_files = [
    # "C:/Users/tian/Desktop/data/water.txt",
    "C:/Users/tian/Desktop/data/zuankong.txt",
    "C:/Users/tian/Desktop/data/EW.txt",
    "C:/Users/tian/Desktop/data/NE.txt",
    # "C:/Users/tian/Desktop/data/NS.txt",
    "C:/Users/tian/Desktop/data/NS_fin.txt",
    "C:/Users/tian/Desktop/data/NW.txt",
]

# 给每个数据文件分配一个颜色
colors = ["black", "red", "blue", "green", "orange"]

# 分配数据文件的名称作为图例
labels = ["Strain", "EW", "NE", "NS", "NW"]

# 可视化处理后的数据
plt.figure(figsize=(18, 9))

# 读取每个数据文件并将结果绘制到图表上
for i, data_file in enumerate(data_files):
    data = read_data_from_file(data_file)
    df = pd.DataFrame(data, columns=["timestamp", "value"])

    # 对数据进行归一化
    normalized_data = normalize_data(df)

    plt.plot(df["timestamp"], normalized_data, color=colors[i], label=labels[i])
    print(f"Processing {data_file}: {len(normalized_data)} data points")
    print(f"Last 5 data points: {normalized_data[-5:]}")

plt.xlabel("Date")
plt.ylabel("Normalized Data")

plt.title("Normalized Data Visualization")
plt.legend(loc="best")  # 添加图例
plt.tight_layout()  # 调整图的大小和边距以使图更紧凑

# 保存 300 dpi 的 jpg 格式图片
# plt.savefig("C:/Users/tian/Desktop/论文绘图/六合一/六合一.jpg", dpi=300)
plt.show()
