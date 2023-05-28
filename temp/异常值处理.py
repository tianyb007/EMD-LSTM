# 这个代码中使用了基于阈值的异常值处理方法。首先，它计算了序列的均值和标准差，
# 然后将大于均值加减 3 倍标准差的数据点设为异常值，并用均值对其进行替代。


import numpy as np
import pandas as pd


# 读取原始数据
data = np.loadtxt('C:/Users/tian/Desktop/data/yuanshi.txt')
time, values = data[:, 0], data[:, 1]

# 定义异常值处理方法


def process_outliers(values):
    threshold = 3.0  # 定义阈值
    mean = np.mean(values)
    std = np.std(values)

    is_outlier = (values - mean).clip(0, np.inf) > threshold * std
    values[is_outlier] = mean

    return values

# 将数据进行异常值处理


values = process_outliers(values)

# 其他代码参照上面的代码示例
resampled_data = np.column_stack((time, values))
np.savetxt('C:/Users/tian/Desktop/data/reprocess.txt', values)
