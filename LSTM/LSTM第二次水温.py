import pandas as pd
# 核心代码，设置显示的最大列、宽等参数，消掉打印不完全中间的省略号
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)

import matplotlib.pyplot as plt
import numpy as np
from pandas import DataFrame
from pandas import concat
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from numpy import concatenate
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from math import sqrt
import matplotlib
import pandas as pd
import os

# 读取文本文件，并将第一列解析为日期时间格式, 并设为索引
data_file = r'C:/Users/tian/Desktop/data/watertest2.txt'
data = pd.read_csv(data_file, sep=' ', header=None, parse_dates=[0], index_col=0)
print(data.head())
# 对数据的列名重新命名
data.columns = ['数据']
data.index.name = '日期'  # 日期为索引列

# 打印数据的前5行
print(data.head())

# 获取DataFrame中的数据，形式为数组array形式
values = data.values
# 确保所有数据为float类型
values = values.astype('float32')

# 特征的归一化处理
scaler = MinMaxScaler(feature_range=(0, 1))
scaled = scaler.fit_transform(values)
print(scaled)

# 定义series_to_supervised()函数
# 将时间序列转换为监督学习问题
def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
	"""
	Frame a time series as a supervised learning dataset.
	Arguments:
		data: Sequence of observations as a list or NumPy array.
		n_in: Number of lag observations as input (X).
		n_out: Number of observations as output (y).
		dropnan: Boolean whether or not to drop rows with NaN values.
	Returns:
		Pandas DataFrame of series framed for supervised learning.
	"""
	n_vars = 1 if type(data) is list else data.shape[1]
	df = DataFrame(data)
	cols, names = list(), list()
	# input sequence (t-n, ... t-1)
	for i in range(n_in, 0, -1):
		cols.append(df.shift(i))
		names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
	# forecast sequence (t, t+1, ... t+n)
	for i in range(0, n_out):
		cols.append(df.shift(-i))
		if i == 0:
			names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
		else:
			names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
	# put it all together
	agg = concat(cols, axis=1)
	agg.columns = names
	# drop rows with NaN values
	if dropnan:
		agg.dropna(inplace=True)
	return agg

# 将时间序列转换为监督学习问题
reframed = series_to_supervised(scaled, 1, 1)

# 划分训练集和测试集
values = reframed.values
n_train = int(len(values) * 0.70)  # 取前70%的数据作为训练集
train = values[:n_train, :]
test = values[n_train:, :]
# 划分训练集和测试集的输入和输出
train_X, train_y = train[:, :-1], train[:, -1]
test_X, test_y = test[:, :-1], test[:, -1]

train_X = train_X.reshape((train_X.shape[0], 1, train_X.shape[1]))
test_X = test_X.reshape((test_X.shape[0], 1, test_X.shape[1]))

# 搭建LSTM模型
model = Sequential()
model.add(LSTM(128, input_shape=(train_X.shape[1], train_X.shape[2])))
model.add(Dropout(0.5))
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='mae', optimizer='adam')
# fit network
history = model.fit(train_X, train_y, epochs=100, batch_size=4096, validation_data=(test_X, test_y), verbose=2,
					shuffle=False)
model.save('C:/Users/tian/Desktop/data/watersigmoid2.h5')

# 计算数据的平均值、标准差、最大值和最小值
data_mean = data['数据'].mean()
data_std = data['数据'].std()
data_min = data['数据'].min()
data_max = data['数据'].max()

print("平均值：", data_mean)
print("标准差：", data_std)
print("最小值：", data_min)
print("最大值：", data_max)

# 绘制损失图
plt.figure()  # 创建新的图形窗口
plt.plot(history.history['loss'], label='train')
plt.plot(history.history['val_loss'], label='test')
plt.title('LSTM predict', fontsize='12')
plt.ylabel('loss', fontsize='10')
plt.xlabel('epoch', fontsize='10')
plt.legend()
plt.show()

# 模型预测目标数据列
y_predict = model.predict(test_X)
test_X = test_X.reshape((test_X.shape[0], test_X.shape[2]))

# invert scaling for forecast
# 将预测结果按比例反归一化
inv_y_test = concatenate((test_X[:, :6], y_predict), axis=1)
inv_y_test = scaler.inverse_transform(inv_y_test)
inv_y_predict = inv_y_test[:, -1]

# invert scaling for actual
# 将真实结果按比例反归一化
test_y = test_y.reshape((len(test_y), 1))
inv_y_train = concatenate((test_X[:, :6], test_y), axis=1)
inv_y_train = scaler.inverse_transform(inv_y_train)
inv_y = inv_y_train[:, -1]
print('反归一化后的预测结果：', inv_y_predict)
print('反归一化后的真实结果：', inv_y)
abs = inv_y_predict - inv_y
print('相对误差水平：', (inv_y_predict - inv_y).sum() / inv_y.sum())

# 计算回归评价指标
# calculate MSE 均方误差
MSE = mean_squared_error(inv_y, inv_y_predict)
# calculate RMSE 均方根误差
RMSE = sqrt(mean_squared_error(inv_y, inv_y_predict))
# calculate MAE 平均绝对误差
MAE = mean_absolute_error(inv_y, inv_y_predict)
# calculate R square
r_square = r2_score(inv_y, inv_y_predict)
print('均方误差: %.6f' % MSE)
print('均方根误差: %.6f' % RMSE)
print('平均绝对误差: %.6f' % MAE)
print('R_square: %.6f' % r_square)

plt.figure(figsize=(18, 9))
plt.plot(inv_y, color='red', label='Original')
plt.plot(inv_y_predict, color='green', label='Predict')
plt.xlabel('Time(minutes)')
plt.ylabel('Temperature/°C')
plt.title('LSTM predict')
plt.legend()
plt.show()
