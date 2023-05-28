# 这段程序是处理钻孔应变的数据，按照年份的数据绘制出图形，并且输出三种格式的图片。输出图片的分辨率是300dpi
# 对于异常值只把999999的值置为NaN,没有进一步处理异常的数据。

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# 读取数据
data_file = "C:/Users/tian/Desktop/zuankong/fenliang/NW_adjusted_3.txt"

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

# 计算开始和结束年份
start_year = df["timestamp"].dt.year.min()
end_year = df["timestamp"].dt.year.max()

# 指定保存图像的路径
output_path = "C:/Users/tian/Desktop/zuankong/pic/NW/"

# 按年份绘制图形
for year in range(start_year, end_year + 1):
    yearly_data = df[df["timestamp"].dt.year == year]

    # 可视化处理后的数据
    fig, ax = plt.subplots(figsize=(18, 9))
    ax.plot(yearly_data["timestamp"], yearly_data["borehole_strain"], color="black", linewidth=0.5, linestyle="solid")

    # 设置x轴日期格式
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.xlabel("Date")
    plt.ylabel("Borehole Strain")
    plt.title(f"NW Borehole Strain Data for {year}")

    # 调整布局以去除多余的白边
    fig.tight_layout()

    # 保存图形为 png、jpeg 和 svg 格式
    # plt.savefig(f"{output_path}borehole_strain_{year}.png", dpi=300)
    plt.savefig(f"{output_path}borehole_strain_{year}.jpeg", dpi=300)
    # plt.savefig(f"{output_path}borehole_strain_{year}.svg", dpi=300)
    # 关闭图形
    plt.close(fig)

    # 若要显示图形，请取消以下注释
    plt.show()
