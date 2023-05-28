import pandas as pd
import numpy as np

data_file = "C:/Users/tian/Desktop/data/ne2009.txt"

with open(data_file, "r") as file:
    lines = file.readlines()

data = []

for line in lines:
    items = line.split()
    date = items[0]
    values = items[1:]

    for idx, value in enumerate(values):
        if value == "NaN":
            value = np.nan
        else:
            value = float(value)

        timestamp = pd.to_datetime(date) + pd.Timedelta(minutes=idx)
        data.append([timestamp, value])

df = pd.DataFrame(data, columns=["timestamp", "water_temperature"])

# 处理NaN值
x = df.index[df['water_temperature'].notna()]
y = df['water_temperature'][df['water_temperature'].notna()]
x_new = df.index[df['water_temperature'].isna()]
y_new = np.interp(x_new, x, y)
df.loc[df['water_temperature'].isna(), 'water_temperature'] = y_new

# 将处理后的数据写入一个新的txt文件
with open("C:/Users/tian/Desktop/data/new.txt", "w") as output_file:
    for index, row in df.iterrows():
        output_file.write(f"{row[0]} {row[1]}\n")
