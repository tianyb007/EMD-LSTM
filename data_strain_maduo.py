# 绘制钻孔应变数据，需要选择合适的文件，修改图的标题和保存的文件名。
# 读取txt文件格式
# 用这个画图是绘制原始数据，单一文件，直接进行展示，主要针对钻孔应变的数据。




import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# 读取数据
# data_file = "C:/Users/tian/Desktop/data/2007.txt"
data_file = "C:/Users/tian/Desktop/zuankong/20210107.txt"
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
        if float(value) == 999999:
            value = np.nan
        else:
            value = float(value)
        # 将分钟数据添加到时间戳中
        timestamp = pd.to_datetime(date) + pd.Timedelta(minutes=idx)
        data.append([timestamp, value])

# 将数据转换为DataFrame
df = pd.DataFrame(data, columns=["timestamp", "borehole_strain"])

# 按时间戳对数据进行排序
df.sort_values(by=["timestamp"], inplace=True)

# 使用线性插值填充缺失值
# df["borehole_strain"].interpolate(method="linear", inplace=True)

# 可视化处理后的数据
fig, ax = plt.subplots(figsize=(18, 9))
ax.plot(df["timestamp"], df["borehole_strain"], color="black", linewidth=0.5, linestyle="solid")

# 设置x轴日期格式
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
# plt.xticks(rotation=45)
plt.xlabel("Date")
plt.ylabel("Borehole Strain")
plt.title("Borehole Strain Data 2021 01-07")
# plt.grid()

# 调整布局以去除多余的白边
fig.tight_layout()

# 保存图像为 png、jpeg 和 svg 格式
output_file_base = "C:/Users/tian/Desktop/zuankong/pic/20210107"
plt.savefig(f"{output_file_base}.png", dpi=300)
plt.savefig(f"{output_file_base}.jpeg", dpi=300)
plt.savefig(f"{output_file_base}.svg", dpi=300)

plt.show()


