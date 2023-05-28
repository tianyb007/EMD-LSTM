import pandas as pd
import matplotlib.pyplot as plt
#
# 读取数据
data = pd.read_csv('C:/Users/tian/Desktop/data/tide.txt', sep='\s+', header=None, usecols=[6], names=['value'])

# 将数据转换为时序数据
index = pd.date_range('2021-06-01 00:01:00', periods=len(data), freq='1min')
ts = pd.Series(data['value'].values, index=index)

# 绘制时序数据
fig, ax = plt.subplots(figsize=(20, 8))
ax.plot(ts)

plt.xlabel('Time(minutes)')
plt.ylabel('Gravity(μGal)')
plt.title('Gravity data with tides removed')

# 显示图形
plt.show()
fig.savefig('C:/Users/tian/Desktop/data/tide.png', dpi=300, bbox_inches='tight')