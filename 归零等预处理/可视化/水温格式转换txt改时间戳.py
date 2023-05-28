import os
import pandas as pd
import numpy as np

data_file = "C:/Users/tian/Desktop/data/day_change_adjusted_all_mod.txt"
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

    # 将值添加到数据列表
    for idx, value in enumerate(values):
        if "NaN" in value:
            value = np.nan
        else:
            value = float(value)
        # 将分钟数据添加到时间戳中
        timestamp = pd.to_datetime(date) + pd.Timedelta(minutes=idx)
        data.append([timestamp, value])

# 将数据转换为 DataFrame
df = pd.DataFrame(data, columns=["timestamp", "value"])

# 对 NaN 值进行插值处理
df["value"].interpolate(method="linear", inplace=True)

# 重新转换为时间戳字符串
df["timestamp"] = df["timestamp"].dt.strftime("%Y%m%d%H%M")

# 将插值处理后的数据写入新的 txt 文件
output_file = "C:/Users/tian/Desktop/data/water20072022.txt"

with open(output_file, "w") as file:
    for _, row in df.iterrows():
        file.write(f"{row['timestamp']} {row['value']:.4f}\n")

print(f"数据已保存到：{os.path.abspath(output_file)}")

