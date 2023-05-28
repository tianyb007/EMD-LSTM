import numpy as np
import matplotlib.pyplot as plt
from PyEMD import EMD
from scipy.signal import detrend
import csv


def read_data(file_path):
    data = []
    with open(file_path, 'r') as f:
        for line in f.readlines():
            _, value = line.strip().split()
            data.append(float(value))
    return np.array(data)


def save_imfs_to_csv(imfs, file_path):
    np.savetxt(file_path, imfs.T, delimiter=',')


def emd_analysis(data):
    emd = EMD()
    imfs = emd(data)
    reconstructed_data = np.sum(imfs, axis=0)
    return imfs, reconstructed_data


def plot_comparison(original_data, reconstructed_data):
    plt.figure(figsize=(12, 6))
    plt.plot(original_data, label='Original Data')
    plt.plot(reconstructed_data, label='Reconstructed Data', linestyle='--')
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.legend()
    plt.show()


def main():
    file_path = 'C:/Users/tian/Desktop/data/wateremd.txt'
    data = read_data(file_path)

    imfs, reconstructed_data = emd_analysis(data)

    # 保存IMFs到CSV文件
    imfs_file_path = 'C:/Users/tian/Desktop/data/imfs.csv'
    save_imfs_to_csv(imfs, imfs_file_path)

    plot_comparison(data, reconstructed_data)


if __name__ == '__main__':
    main()
