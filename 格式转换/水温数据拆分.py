import pandas as pd
import os

# 读取数据
data_file = "C:/Users/tian/Desktop/data/chai/water.txt"
df = pd.read_csv(data_file, delimiter=' ', names=["timestamp", "value"])

# 将时间戳转换为日期格式
df["timestamp"] = pd.to_datetime(df["timestamp"], format="%Y%m%d%H%M")

# 获取年份列表
years = df["timestamp"].dt.year.unique()

# 根据年份拆分数据并保存到单独的文件
for year in years:
    df_year = df[df["timestamp"].dt.year == year]

    # 将拆分后的数据写入新的 txt 文件
    output_file = f"{os.path.splitext(data_file)[0]}_{year}.txt"
    with open(output_file, "w") as file:
        for _, row in df_year.iterrows():
            file.write(f"{row['timestamp'].strftime('%Y%m%d%H%M')} {row['value']:.4f}\n")

    print(f"数据已保存到：{os.path.abspath(output_file)}")
