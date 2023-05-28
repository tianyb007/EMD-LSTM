import pandas as pd
import numpy as np
import math

input_file = "C:/Users/tian/Desktop/data/day_change.txt"
output_file = "C:/Users/tian/Desktop/data/day_change_adjusted_all.txt"

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

# 设置多个时间范围及其对应的常数值
time_periods = [
    {
        'start_date': pd.to_datetime('2012-06-12', format='%Y-%m-%d'),
        'end_date': pd.to_datetime('2012-11-01', format='%Y-%m-%d'),
        'constant': 4.4
    },
    # 添加其他时间段及其对应的常数值
    {
        'start_date': pd.to_datetime('2012-11-02', format='%Y-%m-%d'),
        'end_date': pd.to_datetime('2013-05-05', format='%Y-%m-%d'),
        'constant': 4.465
    },
    {
        'start_date': pd.to_datetime('2013-05-6', format='%Y-%m-%d'),
        'end_date': pd.to_datetime('2017-10-31', format='%Y-%m-%d'),
        'constant': 4.4
    },
    {
        'start_date': pd.to_datetime('2017-11-01', format='%Y-%m-%d'),
        'end_date': pd.to_datetime('2022-12-31', format='%Y-%m-%d'),
        'constant': 0.4
    },
    {
        'start_date': pd.to_datetime('2021-08-28', format='%Y-%m-%d'),
        'end_date': pd.to_datetime('2022-12-31', format='%Y-%m-%d'),
        'constant': 0.04
    }
]

def adjust_water_temperature(row):
    for period in time_periods:
        if period['start_date'] <= row['timestamp'] <= period['end_date'] and not np.isnan(row['water_temperature']):
            return row['water_temperature'] + period['constant']
    return row['water_temperature']

# 对于每个时间范围，检查时间戳是否在指定范围内，如果是，并且值不是NaN，则加上对应的常数
df['adjusted_water_temperature'] = df.apply(adjust_water_temperature, axis=1)

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
