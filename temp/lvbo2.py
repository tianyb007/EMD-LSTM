# 设计一个带通滤波器，滤波频率为0.2-0.5Hz，使用Python
# 我已经有时序数据了，你能把代码改一下吗，从硬盘中导入我的数据，路径我可以自己设置

import numpy as np
import scipy.signal as sig

# 加载数据
data = np.loadtxt('C:/Users/tian/Desktop/data/reprocess.txt')

# 定义滤波器参数
fs = 1000.0       # 采样频率
f1 = 0.2          # 通带最低频率
f2 = 0.5          # 通带最高频率
b, a = sig.butter(6, [2*f1/fs, 2*f2/fs], btype='band')

# 应用滤波器
filtered_data = sig.filtfilt(b, a, data)

# 保存结果
np.savetxt('C:/Users/tian/Desktop/data/filtered_data.txt', filtered_data)














