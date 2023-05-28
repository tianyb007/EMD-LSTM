import pandas as pd
import matplotlib.pyplot as plt

# 读取重采样后的数据
df = pd.read_csv('C:/Users/tian/Desktop/data/resampled_data.txt', sep=' ', header=None, names=['time', 'data'])
df.index = df['time']
df.drop(columns=['time'], inplace=True)

# 绘制时域图
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(df.index, df['data'])
ax.set_xlabel('Time')
ax.set_ylabel('Gravity Data')
plt.show()
