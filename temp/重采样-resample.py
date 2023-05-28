import pandas as pd  # 导入pandas库
import numpy as np  # 导入numpy库

# 读取原始数据文件
data = pd.read_csv('C:/Users/tian/Desktop/data/yuanshidel.txt', delim_whitespace=True,
                   header=None, names=['time', 'gravity'])

# 将时间列转换为秒

data['time_sec'] = data['time'] * 60
print(data['time'])
print(data['time'][0])
for i in range(0, 38880):
    data['time'][i] = (int(str(data['time'][i]) + '00'))
print(data['time'])
print(data['time'][0])
exit()
data['time_sec1'] = int(str(data['time'][-4:]) + '00') * 60
print(data)
exit()
# 通过numpy的interp函数实现线性插值得到2.5Hz的数据列
new_time_sec = np.arange(data['time_sec'].iloc[0], data['time_sec'].iloc[-1], 1 / 2.5)
resampled_data = np.interp(new_time_sec, data['time_sec'], data['gravity'])

# 创建新的DataFrame对象，保存重采样后的数据
resampled = pd.DataFrame({'time_sec': new_time_sec, 'gravity': resampled_data})

# 将结果保存到新的txt文件
resampled.to_csv('C:/Users/tian/Desktop/data/resampled_data.txt', sep='\t', header=None, index=None,
                 float_format='%.2f')
