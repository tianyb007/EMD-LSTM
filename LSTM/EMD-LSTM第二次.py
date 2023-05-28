import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from pandas import DataFrame, concat
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
# 预测IMFs分量并且预测，把预测值保存到csv文件中
# 读取IMFs分量文件
data_file = 'C:/Users/tian/Desktop/data/imfs_trimed.csv'
data = pd.read_csv(data_file, skiprows=0)

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
        names += [('var%d(t-%d)' % (j + 1, i)) for j in range(n_vars)]
    # forecast sequence (t, t+1, ... t+n)
    for i in range(0, n_out):
        cols.append(df.shift(-i))
        if i == 0:
            names += [('var%d(t)' % (j + 1)) for j in range(n_vars)]
        else:
            names += [('var%d(t+%d)' % (j + 1, i)) for j in range(n_vars)]
    # put it all together
    agg = concat(cols, axis=1)
    agg.columns = names
    # drop rows with NaN values
    if dropnan:
        agg.dropna(inplace=True)
    return agg

predicted_data = []

for i in range(num_columns):
    column_data = data.iloc[:, i].values.reshape(-1, 1)
    # scaler = MinMaxScaler(feature_range=(0, 1))
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(column_data)
    reframed_data = series_to_supervised(scaled_data, 1, 1)
    values = reframed_data.values

    n_train = int(0.6 * len(values))
    n_val = int(0.8 * len(values))
    train = values[:n_train, :]
    val = values[n_train:n_val, :]
    test = values[n_val:, :]

    train_X, train_y = train[:, :-1], train[:, -1]
    val_X, val_y = val[:, :-1], val[:, -1]
    test_X, test_y = test[:, :-1], test[:, -1]

    train_X = train_X.reshape((train_X.shape[0], 1, train_X.shape[1]))
    val_X = val_X.reshape((val_X.shape[0], 1, val_X.shape[1]))
    test_X = test_X.reshape((test_X.shape[0], 1, test_X.shape[1]))

    model = Sequential()
    model.add(LSTM(128, activation='relu', input_shape=(train_X.shape[1], train_X.shape[2])))
    model.add(Dropout(0.5))
    model.add(Dense(1))
    model.compile(loss='mae', optimizer='sgd')

    model.fit(train_X, train_y, epochs=100, batch_size=4096, validation_data=(val_X, val_y), verbose=2, shuffle=False)

    column_prediction = model.predict(test_X)
    inv_column_prediction = scaler.inverse_transform(column_prediction)

    predicted_data.append(inv_column_prediction)

# 将预测结果转换为DataFrame
predicted_data_df = pd.DataFrame(np.hstack(predicted_data),
                                 columns=[f'IMFs{i}_Prediction' for i in range(1, num_columns + 1)])

# 保存预测结果到CSV文件
predicted_data_df.to_csv('C:/Users/tian/Desktop/data/predicted_data2.csv', index=False)

fig, axes = plt.subplots(num_columns, 1, figsize=(12, num_columns * 4))
for i in range(num_columns):
    column_data = data.iloc[:, i].values.reshape(-1, 1)
    original_test = column_data[n_val:]
    axes[i].plot(original_test, label='Original', color='red')
    axes[i].plot(predicted_data[i], label='Predicted', color='blue')
    axes[i].set_title(f'IMFs{i + 1} Original vs. Predicted')
    axes[i].legend()