import pandas as pd
import numpy as np
# import math
input_file = "C:/Users/tian/Desktop/data/zuankong_adjusted_mod.txt"
output_file = "C:/Users/tian/Desktop/data/zuankong_adjusted_mod_1.txt"

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

thresholds = [
    {
        'start_date': pd.to_datetime('2007-08-01', format='%Y-%m-%d'),
        'end_date': pd.to_datetime('2007-09-01', format='%Y-%m-%d'),
        'max_value': 80000,
        'mim_value': 40000
    },
{
        'start_date': pd.to_datetime('2008-12-01', format='%Y-%m-%d'),
        'end_date': pd.to_datetime('2008-12-31', format='%Y-%m-%d'),
        'max_value': 60000,
        'mim_value': 10000
    },
    {
        'start_date': pd.to_datetime('2009-11-01', format='%Y-%m-%d'),
        'end_date': pd.to_datetime('2009-12-31', format='%Y-%m-%d'),
        'max_value': 10000,
        'mim_value': 0
    },
    {
        'start_date': pd.to_datetime('2010-01-01', format='%Y-%m-%d'),
        'end_date': pd.to_datetime('2010-04-10', format='%Y-%m-%d'),
        'max_value': 10000,
        'mim_value': -10000
    },
    {
        'start_date': pd.to_datetime('2010-06-22', format='%Y-%m-%d'),
        'end_date': pd.to_datetime('2010-09-01', format='%Y-%m-%d'),
        'max_value': -10000,
        'mim_value': -30000
    },
    {
        'start_date': pd.to_datetime('2011-01-01', format='%Y-%m-%d'),
        'end_date': pd.to_datetime('2011-12-29', format='%Y-%m-%d'),
        'max_value': 40000,
        'mim_value': 80000
    },
    {
        'start_date': pd.to_datetime('2012-09-01', format='%Y-%m-%d'),
        'end_date': pd.to_datetime('2011-12-29', format='%Y-%m-%d'),
        'max_value': 40000,
        'mim_value': 80000
    },
    {
        'start_date': pd.to_datetime('2014-01-01', format='%Y-%m-%d'),
        'end_date': pd.to_datetime('2014-05-29', format='%Y-%m-%d'),
        'max_value': 40000,
        'mim_value': 80000
    }
]


def apply_thresholds(row):
    for threshold in thresholds:
        if (threshold['start_date'] <= row['timestamp'] <= threshold['end_date'] and
            (row['adjusted_strain'] < threshold['min_value'] or row['adjusted_strain'] > threshold['max_value'])):
            return np.nan
    return row['adjusted_strain']

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
