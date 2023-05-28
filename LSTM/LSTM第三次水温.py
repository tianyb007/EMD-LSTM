import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame
from pandas import concat
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from numpy import concatenate
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from math import sqrt

data_file = r'C:/Users/tian/Desktop/data/watertest2.txt'
data = pd.read_csv(data_file, sep=' ', header=None, parse_dates=[0], index_col=0)
data.columns = ['数据']
data.index.name = '日期'

values = data.values
values = values.astype('float32')

scaler = MinMaxScaler(feature_range=(0, 1))
scaled = scaler.fit_transform(values)

def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
    n_vars = 1 if type(data) is list else data.shape[1]
    df = DataFrame(data)
    cols, names = list(), list()
    for i in range(n_in, 0, -1):
        cols.append(df.shift(i))
        names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
    for i in range(0, n_out):
        cols.append(df.shift(-i))
        if i == 0:
            names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
        else:
            names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
    agg = concat(cols, axis=1)
    agg.columns = names
    if dropnan:
        agg.dropna(inplace=True)
    return agg

reframed = series_to_supervised(scaled, 1, 1)

values = reframed.values
# n_train = int(len(values) * 0.6)
# n_val = int(len(values) * 0.2)
n_train = 262144
n_val = 81920
train = values[:n_train, :]
val = values[n_train:n_train+n_val, :]
test = values[n_train+n_val:, :]
train_X, train_y = train[:, :-1], train[:, -1]
val_X, val_y = val[:, :-1], val[:, -1]
test_X, test_y = test[:, :-1], test[:, -1]

train_X = train_X.reshape((train_X.shape[0], 1, train_X.shape[1]))
val_X = val_X.reshape((val_X.shape[0], 1, val_X.shape[1]))
test_X = test_X.reshape((test_X.shape[0], 1, test_X.shape[1]))

model = Sequential()
model.add(LSTM(128, batch_input_shape=(4096, train_X.shape[1], train_X.shape[2]), stateful=True))
model.add(Dropout(0.5))
model.add(Dense(1, activation='relu'))
model.compile(loss='mae', optimizer='sgd')

epochs = 50
for i in range(epochs):
    model.fit(train_X, train_y, epochs=1, batch_size=4096, validation_data=(val_X, val_y), verbose=2, shuffle=False)
    model.reset_states()

# 创建具有相同架构但不同批次大小的新模型
predict_model = Sequential()
predict_model.add(LSTM(128, batch_input_shape=(1, train_X.shape[1], train_X.shape[2]), stateful=True))
predict_model.add(Dropout(0.5))
predict_model.add(Dense(1, activation='sigmoid'))
predict_model.compile(loss='mae', optimizer='adam')

# 将训练好的权重复制到新模型
predict_model.set_weights(model.get_weights())

y_predict = predict_model.predict(test_X, batch_size=1)

test_X = test_X.reshape((test_X.shape[0], test_X.shape[2]))

inv_y_test = concatenate((test_X[:, :6], y_predict), axis=1)
inv_y_test = scaler.inverse_transform(inv_y_test)
inv_y_predict = inv_y_test[:, -1]

test_y = test_y.reshape((len(test_y), 1))
inv_y_train = concatenate((test_X[:, :6], test_y), axis=1)
inv_y_train = scaler.inverse_transform(inv_y_train)
inv_y = inv_y_train[:, -1]

model.save('C:/Users/tian/Desktop/data/waterstateful1.h5')

# 计算数据的平均值、标准差、最大值和最小值
data_mean = data['数据'].mean()
data_std = data['数据'].std()
data_min = data['数据'].min()
data_max = data['数据'].max()
print("平均值：", data_mean)
print("标准差：", data_std)
print("最小值：", data_min)
print("最大值：", data_max)

MSE = mean_squared_error(inv_y, inv_y_predict)
RMSE = sqrt(mean_squared_error(inv_y, inv_y_predict))
MAE = mean_absolute_error(inv_y, inv_y_predict)
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



