import pandas as pd

# 读取CSV文件
file_path = 'C:/Users/tian/Desktop/data/imfs_trimed.csv'
data = pd.read_csv(file_path)

# 定义要删除的前n行和后m行
# n = 14400  # 例如，删除前10行
# m = 14400  # 例如，删除后10行
# 删除前面的数据
n = 244224  # 例如，删除前10行
# 删除前n行和后m行
# data_trimmed = data.iloc[n:-m]
data_trimmed = data.iloc[n:]
# 保存处理后的CSV文件
output_file_path = 'C:/Users/tian/Desktop/data/imfs_zhong.csv'
data_trimmed.to_csv(output_file_path, index=False)
