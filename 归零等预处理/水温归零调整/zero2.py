# 这是调整数据归零的操作，并且调整之后和原始数据的格式是一样的。
# 根据每份数据的不同，需要调整的时间段也不相同，应该为每份数据单独写一份代码，省的来回改。
# 这份是根据水温数据进行编写的，需要调整阶段时间段的不同，自行修改时间段的代码。


import pandas as pd
import numpy as np
import math

input_file = "C:/Users/tian/Desktop/data/day_change.txt"
output_file = "C:/Users/tian/Desktop/data/day_change_adjusted.txt"

with open(input_file, "r") as file:
    lines = file.readlines()

data = []

for line in lines:
    items = line.split()
    date = pd.to_datetime(items[0], format='%Y%m%d')
    for i in range(1, len(items)):
        timestamp = date + pd.Timedelta(minutes=(i - 1))
        value = float(items[i]) if float(items[i]) <= 14 else np.nan
        data.append([timestamp, value])

df = pd.DataFrame(data, columns=["timestamp", "water_temperature"])

# 设置时间范围
start_date = pd.to_datetime('2012-06-12', format='%Y-%m-%d')
end_date = pd.to_datetime('2017-10-31', format='%Y-%m-%d')

# 设置要添加的常数值
constant = 4.4

# 检查时间戳是否在指定的时间范围内，如果是，并且值不是NaN，则加上常数
df['adjusted_water_temperature'] = df.apply(
    lambda row: row['water_temperature'] + constant if start_date <= row['timestamp'] <= end_date and not np.isnan(
        row['water_temperature']) else row['water_temperature'], axis=1)

with open(output_file, 'w') as file:
    current_date = df.iloc[0]['timestamp'].date()
    file.write(str(current_date).replace('-', ''))

    for idx, row in df.iterrows():
        timestamp, water_temperature = row['timestamp'], row['adjusted_water_temperature']

        if timestamp.date() != current_date:
            current_date = timestamp.date()
            file.write('\n' + str(current_date).replace('-', ''))

        if pd.isna(water_temperature):
            file.write(" NaN")
        else:
            file.write(f" {water_temperature:.4f}")
