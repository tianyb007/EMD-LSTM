import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from math import sqrt

# 读取IMFs分量文件
imfs_file = 'C:/Users/tian/Desktop/data/predicted_data2.csv'
imfs_data = pd.read_csv(imfs_file, skiprows=0)

# 叠加IMFs分量，并将结果与原始信号进行比较
reconstructed_signal = np.sum(imfs_data, axis=1)

# 读取原始数据
original_data_file = r'C:/Users/tian/Desktop/data/imfs_zhong.csv'
original_data = pd.read_csv(original_data_file)
original_values = np.sum(imfs_data, axis=1)

# 计算回归评价指标
MSE = mean_squared_error(original_values, reconstructed_signal)
RMSE = sqrt(mean_squared_error(original_values, reconstructed_signal))
MAE = mean_absolute_error(original_values, reconstructed_signal)
r_square = r2_score(original_values, reconstructed_signal)

print('均方误差: %.6f' % MSE)
print('均方根误差: %.6f' % RMSE)
print('平均绝对误差: %.6f' % MAE)
print('R_square: %.6f' % r_square)

# 绘制原始信号和重构信号的对比图
plt.figure(figsize=(18, 9))
plt.plot(original_values, color='red', label='Original')
plt.plot(reconstructed_signal, color='green', label='Reconstructed')
plt.xlabel('Time(minutes)')
plt.ylabel('Temperature/°C')
plt.title('IMFs Prediction')
plt.legend()
plt.show()
