import pandas as pd
import matplotlib.pyplot as plt

# 读取文件并转化为DataFrame数据类型
df = pd.read_csv('C:/Users/tian/Desktop/data/yuanshi.txt', header=None, delimiter='\t', names=['time', 'data'], parse_dates=['time'])

# 根据时间戳对数据进行排序，确保绘图正确
df = df.sort_values(by=['time'])

# 计算均值和标准差
mean = df['data'].mean()
std = df['data'].std()

# 剔除异常数据
df = df[(df['data'] > mean - 3*std) & (df['data'] < mean + 3*std)]
# 这里我们定义了一个区间，区间的范围是均值加减3倍标准差。数据点如果不在这个区间里面，就被认为是异常值，我们将这些异常值从数据框中剔除

# 设置绘图大小和线条样式
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(df['time'], df['data'], linestyle='-', color='red', linewidth=2)

# 设置横轴标签和刻度间隔
ax.set_xlabel('Time', fontsize=14)
ax.xaxis.set_major_locator(plt.MaxNLocator(10)) # 设置X轴刻度间隔为10

# 设置纵轴标签和刻度间隔
ax.set_ylabel('Data', fontsize=14)
y_ticks = ax.get_yticks()
ax.set_yticklabels([f'{int(tick):d}' for tick in y_ticks])

# 设置标题
plt.title('Processed Data')

# 显示图形
plt.show()

# 保存处理过的数据
# df.to_csv('C:/Users/tian/Desktop/data/new_file.txt', sep='\t', header=None, index=False, encoding='utf-8')

with open('C:/Users/tian/Desktop/data/new_file.txt', 'w') as f:
    for index, row in df.iterrows():
        line = '\t'.join([str(row[0]), str(row[1])]) + '\n'
        print(line)
        exit(0)
        f.write(line)














