import pandas as pd
import numpy as np
import math

input_file = "C:/Users/tian/Desktop/data/fenliang/NS.txt"
output_file = "C:/Users/tian/Desktop/data/fenliang/NS_adjusted_1.txt"

with open(input_file, "r") as file:
    lines = file.readlines()

data = []

for line in lines:
    items = line.split()
    date = pd.to_datetime(items[0], format='%Y%m%d')
    for i in range(1, len(items)):
        timestamp = date + pd.Timedelta(minutes=(i - 1))
        value = float(items[i]) if float(items[i]) <= 350000 else np.nan
        data.append([timestamp, value])

df = pd.DataFrame(data, columns=["timestamp", "strain"])

# 设置多个时间范围及其对应的常数值
time_periods = [
    {
        'start_date': pd.to_datetime('2021-11-01', format='%Y-%m-%d'),
        'end_date': pd.to_datetime('2022-09-01', format='%Y-%m-%d'),
        'constant': -20357
    },
    {
        'start_date': pd.to_datetime('2007-01-01', format='%Y-%m-%d'),
        'end_date': pd.to_datetime('2007-12-30', format='%Y-%m-%d'),
        'constant': 87896
    },
    # 添加其他时间段及其对应的常数值，
    {
        'start_date': pd.to_datetime('2009-06-24', format='%Y-%m-%d'),
        'end_date': pd.to_datetime('2009-12-30', format='%Y-%m-%d'),
        'constant': -40325
    },
    {
        'start_date': pd.to_datetime('2010-04-15', format='%Y-%m-%d'),
        'end_date': pd.to_datetime('2011-01-30', format='%Y-%m-%d'),
        'constant': -85516
    },
    {
        'start_date': pd.to_datetime('2013-08-09', format='%Y-%m-%d'),
        'end_date': pd.to_datetime('2014-04-05', format='%Y-%m-%d'),
        'constant': -57682
    },
    {
        'start_date': pd.to_datetime('2012-01-01', format='%Y-%m-%d'),
        'end_date': pd.to_datetime('2012-12-30', format='%Y-%m-%d'),
        'constant': 15339
    }
]

def adjust_strain(row):
    for period in time_periods:
        if period['start_date'] <= row['timestamp'] <= period['end_date'] and not np.isnan(row['strain']):
            return row['strain'] + period['constant']
    return row['strain']

# 对于每个时间范围，检查时间戳是否在指定范围内，如果是，并且值不是NaN，则加上对应的常数
df['adjusted_strain'] = df.apply(adjust_strain, axis=1)

with open(output_file, 'w') as file:
    current_date = df.iloc[0]['timestamp'].date()
    file.write(str(current_date).replace('-', ''))

    for idx, row in df.iterrows():
        timestamp, strain = row['timestamp'], row['adjusted_strain']

        if timestamp.date() != current_date:
            current_date = timestamp.date()
            file.write('\n' + str(current_date).replace('-', ''))

        if pd.isna(strain):
            file.write(" NaN")
        else:
            file.write(f" {strain:.1f}")
