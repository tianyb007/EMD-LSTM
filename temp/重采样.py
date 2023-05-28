# 一分钟采样一次的数据意味着采样频率为1/60 Hz=0.0167 Hz，如果要对其进行0.2-0.5 Hz的带通滤波，
# 需要先对数据进行重采样，将采样频率提高到至少2.5 Hz以上

# 你可以使用resample函数从scipy的signal模块对你的数据进行重采样处理

import numpy as np
import pandas as pd
from scipy import signal

# 读取原始数据
df = pd.read_csv('C:/Users/tian/Desktop/data/reprocess.csv')

# 将时间序列转换为时间索引
df['Time'] = pd.to_datetime(df['Time'])
df.set_index('Time', inplace=True)

# 设定重采样的目标采样频率
target_fs = 2.5

# 计算重采样前后的采样频率比率
fs = 1.0 / (df.index[1] - df.index[0]).total_seconds()
resample_ratio = target_fs / fs

# 使用signal模块中的resample函数进行重采样
resampled_df = pd.DataFrame(signal.resample(df, int(len(df) * resample_ratio)), columns=df.columns, index=pd.date_range(df.index[0], df.index[-1], freq=str(1.0/target_fs)+'S', closed='left'))

# 保存重采样结果
resampled_df.to_csv('C:/Users/tian/Desktop/data/resampled_data.csv')






