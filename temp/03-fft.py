import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 读取数据
data = pd.read_csv('C:/Users/tian/Desktop/data/tide.txt', sep='\s+', header=None, usecols=[6], names=['value'])

# 将数据转换为时序数据
index = pd.date_range('2021-06-01 00:01:00', periods=len(data), freq='1min')
ts = pd.Series(data['value'].values, index=index)

# 对时序数据进行重采样
new_freq = '400ms'  # 新的采样频率为每400毫秒一次
ts_resampled = ts.resample(new_freq).mean()

# 对重采样后的数据进行傅里叶变换
Fs = 2.5  # 重采样后的采样频率为每2.5秒一次
n = len(ts_resampled)
yf = np.fft.fft(ts_resampled.values)
xf = np.linspace(0.0, 1.0/(2*Fs), n//2)

# 绘制频谱图
fig, ax = plt.subplots()
ax.plot(xf, 2.0/n * np.abs(yf[:n//2]))
ax.set_xlabel('Frequency (cycles/sec)')
ax.set_ylabel('Amplitude')
plt.show()
ts_resampled.to_csv('C:/Users/tian/Desktop/data/resampled_data.csv', header=['value'])