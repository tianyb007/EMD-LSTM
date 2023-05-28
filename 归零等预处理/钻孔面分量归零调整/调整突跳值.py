import pandas as pd
import numpy as np
import math

input_file = "C:/Users/tian/Desktop/data/zuankong_adjusted_4.txt"
output_file = "C:/Users/tian/Desktop/data/zuankong_adjusted_5.txt"

with open(input_file, "r") as file:
    lines = file.readlines()

data = []

for line in lines:
    items = line.split()
    date = pd.to_datetime(items[0], format='%Y%m%d')
    for i in range(1, len(items)):
        timestamp = date + pd.Timedelta(minutes=(i - 1))
        value = float(items[i]) if float(items[i]) <= 110000 else np.nan
        data.append([timestamp, value])

df = pd.DataFrame(data, columns=["timestamp", "strain"])

# 设置多个时间范围及其对应的常数值
time_periods = [
    {
        'start_date': pd.to_datetime('2007-01-01', format='%Y-%m-%d'),
        'end_date': pd.to_datetime('2011-02-27', format='%Y-%m-%d'),
        'constant': 63725
    },
    {
        'start_date': pd.to_datetime('2014-04-21', format='%Y-%m-%d'),
        'end_date': pd.to_datetime('2022-12-29', format='%Y-%m-%d'),
        'constant': -11419
    }

]


def adjust_strain(row):
    for period in time_periods:
        if period['start_date'] <= row['timestamp'] <= period['end_date'] and not np.isnan(row['strain']):
            return row['strain'] + period['constant']
    return row['strain']



thresholds = [
    {
        'start_date': pd.to_datetime('2007-08-01', format='%Y-%m-%d'),
        'end_date': pd.to_datetime('2007-09-01', format='%Y-%m-%d'),
        'min_value': 40000,
        'max_value': 80000
    },
    {
        'start_date': pd.to_datetime('2009-11-01', format='%Y-%m-%d'),
        'end_date': pd.to_datetime('2022-12-29', format='%Y-%m-%d'),
        'min_value': 200,
        'max_value': 8000
    },
    {
        'start_date': pd.to_datetime('2010-01-01', format='%Y-%m-%d'),
        'end_date': pd.to_datetime('2010-08-29', format='%Y-%m-%d'),
        'min_value': -30000,
        'max_value': 10000
    },
    {
        'start_date': pd.to_datetime('2011-01-01', format='%Y-%m-%d'),
        'end_date': pd.to_datetime('2011-12-29', format='%Y-%m-%d'),
        'min_value': -60000,
        'max_value': -27800
    },
    {
        'start_date': pd.to_datetime('2012-09-01', format='%Y-%m-%d'),
        'end_date': pd.to_datetime('2011-12-29', format='%Y-%m-%d'),
        'min_value': -90000,
        'max_value': -63000
    },
    {
        'start_date': pd.to_datetime('2014-01-01', format='%Y-%m-%d'),
        'end_date': pd.to_datetime('2014-05-29', format='%Y-%m-%d'),
        'min_value': -75000,
        'max_value': -80000
    }
]


def apply_thresholds(row):
    for threshold in thresholds:
        if (threshold['start_date'] <= row['timestamp'] <= threshold['end_date'] and
            (row['adjusted_strain'] < threshold['min_value'] or row['adjusted_strain'] > threshold['max_value'])):
            return np.nan
    return row['adjusted_strain']



# 对于每个时间范围，检查时间戳是否在指定范围内，如果是，并且值不是NaN，则加上对应的常数
df['adjusted_strain'] = df.apply(adjust_strain, axis=1)


df['final_strain'] = df.apply(apply_thresholds, axis=1)




with open(output_file, 'w') as file:
    current_date = df.iloc[0]['timestamp'].date()
    file.write(str(current_date).replace('-', ''))

    for idx, row in df.iterrows():
        timestamp, strain = row['timestamp'], row['final_strain']

        if timestamp.date() != current_date:
            current_date = timestamp.date()
            file.write('\n' + str(current_date).replace('-', ''))

        if pd.isna(strain):
            file.write(" NaN")
        else:
            file.write(f" {strain:.1f}")
