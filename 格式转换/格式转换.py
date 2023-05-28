import pandas as pd

data_file = "C:/Users/tian/Desktop/data/strain2010.txt"

with open(data_file, "r") as file:
    lines = file.readlines()

data = []

for line in lines:
    items = line.split()
    date = items[0]
    values = items[1:]

    for idx, value in enumerate(values):
        value = float(value)
        timestamp = pd.to_datetime(date) + pd.Timedelta(minutes=idx)
        data.append([timestamp, value])

# 将数据转换为DataFrame，并将其写入一个新的CSV文件
df = pd.DataFrame(data, columns=["timestamp", "value"])
df.to_csv("C:/Users/tian/Desktop/data/new_data_format.csv", index=False)
 