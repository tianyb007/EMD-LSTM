import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from math import sqrt


def read_original_data(file_path):
    original_data = pd.read_csv(file_path, delimiter=' ', usecols=[1])
    return original_data.values.ravel()


def read_imfs_data(file_path):
    imfs_data = pd.read_csv(file_path)
    return imfs_data.values


def calculate_metrics(original_values, reconstructed_signal):
    MSE = mean_squared_error(original_values, reconstructed_signal)
    RMSE = sqrt(mean_squared_error(original_values, reconstructed_signal))
    MAE = mean_absolute_error(original_values, reconstructed_signal)
    r_square = r2_score(original_values, reconstructed_signal)

    print('均方误差: %.6f' % MSE)
    print('均方根误差: %.6f' % RMSE)
    print('平均绝对误差: %.6f' % MAE)
    print('R_square: %.6f' % r_square)


def plot_comparison(original_data, reconstructed_data):
    plt.figure(figsize=(18, 9))
    plt.plot(original_data, color='red', label='Original')
    plt.plot(reconstructed_data, color='green', label='Reconstructed')
    plt.xlabel('Time(minutes)')
    plt.ylabel('Temperature/°C')
    plt.title('IMFs Reconstruction')
    plt.legend()
    plt.show()


def main():
    original_data_file = r'C:/Users/tian/Desktop/data/wateremd_zong.txt'
    original_values = read_original_data(original_data_file)

    imfs_file = 'C:/Users/tian/Desktop/data/imfs_trimed.csv'
    imfs_data = read_imfs_data(imfs_file)
    reconstructed_signal = np.sum(imfs_data, axis=1)

    # 将原始数据的均值添加到重构信号
    # original_mean = np.mean(original_values)
    # reconstructed_signal += 0.00

    # 计算回归评价指标
    calculate_metrics(original_values, reconstructed_signal)

    # 绘制原始信号和重构信号的对比图
    plot_comparison(original_values, reconstructed_signal)


if __name__ == '__main__':
    main()
