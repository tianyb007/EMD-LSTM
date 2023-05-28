import pandas as pd
import matplotlib.pyplot as plt
import math
import matplotlib.ticker as ticker
# 读取原始IMFs分量数据
file_path_original = 'C:/Users/tian/Desktop/data/imfs_zhong.csv'
original_data = pd.read_csv(file_path_original)

# 读取预测的IMFs分量数据
file_path_predicted = 'C:/Users/tian/Desktop/data/predicted_data2.csv'
predicted_data = pd.read_csv(file_path_predicted, skiprows=0)

# 获取列数
num_columns = original_data.shape[1]

# 创建子图
fig, axes = plt.subplots(math.ceil(num_columns / 2), 2, figsize=(20, 12 * math.ceil(num_columns / 2)))
axs = axes.ravel()
plt.subplots_adjust(hspace=1)
for i in range(num_columns):
    # 获取原始数据和预测数据的对应列
    original_column_data = original_data.iloc[:, i]
    predicted_column_data = predicted_data.iloc[:, i]

    # 获取当前子图的行和列索引
    row_idx = i // 2
    col_idx = i % 2

    # 绘制原始数据和预测数据的曲线图
    axes[row_idx, col_idx].plot(original_column_data, label='Original', color='red')
    axes[row_idx, col_idx].plot(predicted_column_data, label='Predicted', color='green')
    # axes[row_idx, col_idx].set_title(f'IMFs{i + 1} Original vs. Predicted')
    # axes[row_idx, col_idx].legend()
    formatter = ticker.ScalarFormatter(useMathText=True)
    formatter.set_scientific(True)
    formatter.set_powerlimits((-1, 1))
    axes[row_idx, col_idx].yaxis.set_major_formatter(formatter)

# 隐藏多余的子图
for i in range(num_columns, len(axs)):
    axs[i].axis('off')

# 调整子图间距
# plt.tight_layout()

# 显示图形
plt.show()
