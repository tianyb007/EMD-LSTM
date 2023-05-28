import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# 读取CSV文件
# file_path = 'C:/Users/tian/Desktop/data/predicted_data2.csv'
file_path = 'C:/Users/tian/Desktop/data/imfs_zhong.csv'
data = pd.read_csv(file_path, skiprows=0)


# 计算子图布局
num_columns = len(data.columns)
num_rows = num_columns // 2 + (num_columns % 2)

# 创建子图
fig, axs = plt.subplots(num_rows, 2, figsize=(12, num_rows * 4))
axs = axs.ravel()

# 定义子图标题
titles = [f'IMFs{i}' for i in range(1, num_columns + 1)]

# 绘制每一列数据的曲线图并设置标题
for i, (column, title) in enumerate(zip(data.columns, titles)):
    axs[i].plot(data[column])
    axs[i].set_title(title)
    axs[i].set_ylabel(' ')

    # 使用科学计数法格式化纵坐标轴标签
    formatter = ticker.ScalarFormatter(useMathText=True)
    formatter.set_scientific(True)
    formatter.set_powerlimits((-1, 1))
    axs[i].yaxis.set_major_formatter(formatter)

    # 隐藏次要纵坐标刻度
    axs[i].yaxis.set_minor_formatter(ticker.NullFormatter())

# 隐藏多余的子图
for i in range(num_columns, len(axs)):
    axs[i].axis('off')

plt.subplots_adjust(hspace=1.5)
# plt.subplots_adjust(wspace=0.4)
plt.ylabel('tem')
plt.show()
