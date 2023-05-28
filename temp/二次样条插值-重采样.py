# 我需要使用二次样条插值的方法，你重新写一下，我的数据文件格式是txt格式的，总共有两列，第一列是时间，第二列是数据

import numpy as np
import pandas as pd
from scipy.interpolate import interp1d

# 读取原始数据
data = np.loadtxt('C:/Users/tian/Desktop/data/yuanshi.txt')
time, values = data[:, 0], data[:, 1]


# 将时间序列转换为时间索引
time_index = pd.to_datetime(time, unit='s')

# 设定重采样的目标采样频率
target_fs = 2.5

# 基于二次样条插值方法进行重采样
f = interp1d((time - time[0]) / np.timedelta64(1, 's'), values, kind='quadratic')
resampled_values = f(np.arange(0, (time[-1] - time[0]) / np.timedelta64(1, 's'), 1/target_fs))

# 构造重采样时间序列
resampled_time_index = pd.date_range(start=time_index.iloc[0], end=time_index.iloc[-1], periods=len(resampled_values))

# 将重采样后的数据保存到文件中
resampled_data = np.column_stack((resampled_time_index, resampled_values))
np.savetxt('C:/Users/tian/Desktop/data/resampled_data.txt', resampled_data)






















