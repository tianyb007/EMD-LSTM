import pandas as pd
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
from pandas import DataFrame
from pandas import concat
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from numpy import concatenate

# 读取数据
data = pd.read_csv(r'C:/Users/tian/Desktop/data/IMFs_wateremd_trimmed.csv', skiprows=1)

# 获取列数
num_columns = data.shape[1]

# 将时间序列转换为监督学习问题
def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
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

# 对每一列的数据进行预测
predicted_data = []

# ...
for i in range(num_columns):
    column_data = data.iloc[:, i].values.reshape(-1, 1)
    # 将数据归一化
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(column_data)

    # 划分数据集和调用之前定义的series_to_supervised()函数
    reframed_data = series_to_supervised(scaled_data, 1, 1)
    values = reframed_data.values

    # 划分训练集、验证集、测试集
    n_train = int(0.65 * len(values))
    n_val = int(0.85 * len(values))
    train = values[:n_train, :]
    val = values[n_train:n_val, :]
    test = values[n_val:, :]

    # 划分输入和输出
    train_X, train_y = train[:, :-1], train[:, -1]
    val_X, val_y = val[:, :-1], val[:, -1]
    test_X, test_y = test[:, :-1], test[:, -1]

    # 调整数据形状以适应LSTM
    train_X = train_X.reshape((train_X.shape[0], 1, train_X.shape[1]))
    val_X = val_X.reshape((val_X.shape[0], 1, val_X.shape[1]))
    test_X = test_X.reshape((test_X.shape[0], 1, test_X.shape[1]))

    # 创建模型
    model = Sequential()
    model.add(LSTM(128, input_shape=(train_X.shape[1], train_X.shape[2]), activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1))
    model.compile(loss='mae', optimizer='sgd')

    # 训练模型
    model.fit(train_X, train_y, epochs=100, batch_size=4096, validation_data=(val_X, val_y), verbose=2, shuffle=False)

    # 使用模型进行预测
    # column_prediction = model.predict(test_X)
    column_prediction = model.predict(val_X)
    # 反归一化
    test_X = test_X.reshape((test_X.shape[0], test_X.shape[2]))
    inv_y_test = concatenate((test_X, column_prediction), axis=1)
    inv_y_test = scaler.inverse_transform(inv_y_test)
    inv_column_prediction = inv_y_test[:, -1]

    # 将预测结果追加到预测数据列表中
    predicted_data.append(inv_column_prediction)

data_mean_test = -21475.96
# 将预测结果叠加起来
combined_prediction_pre = np.sum(predicted_data, axis=0)
# 将预测结果加上均值，得到最终预测结果
combined_prediction = combined_prediction_pre + np.full(combined_prediction_pre.shape, data_mean_test)

# 提取测试集的真实值
true_values_test = true_values.iloc[n_train:n_val, 0].values

# 计算预测误差
MSE = mean_squared_error(true_values_test, combined_prediction)
RMSE = sqrt(MSE)
MAE = mean_absolute_error(true_values_test, combined_prediction)
r_square = r2_score(true_values_test, combined_prediction)
# 计算数据的平均值、标准差、最大值和最小值
# data_mean = data['数据'].mean()
# data_std = data['数据'].std()
# data_min = data['数据'].min()
# data_max = data['数据'].max()

# print("平均值：", data_mean)
# print("标准差：", data_std)
# print("最小值：", data_min)
# print("最大值：", data_max)
print('均方误差: %.6f' % MSE)
print('均方根误差: %.6f' % RMSE)
print('平均绝对误差: %.6f' % MAE)
print('R_square: %.6f' % r_square)

# 绘制预测结果与实际值对比图
plt.figure(figsize=(18, 9))
plt.plot(true_values_test, color='red', label='Original')
plt.plot(combined_prediction, color='green', label='Predict')
plt.xlabel('Time(minutes)')
plt.ylabel('Temperature/°C')
plt.title('LSTM predict')
plt.legend()
plt.show()

