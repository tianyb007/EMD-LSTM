# 这个是对原始数据可视化，并且计算了日均值进行对比，但是读取的CSV文件。


import pandas as pd
import matplotlib.pyplot as plt

# 读取 CSV 文件
file_path = "C:/Users/tian/Desktop/data/data_maduo.csv"  # 请替换为实际文件路径
data = pd.read_csv(file_path, parse_dates=["timestamp"])

# 计算每日平均水温
data["date"] = data["timestamp"].dt.date
daily_avg_temp = data.groupby("date")["water_temperature"].mean().reset_index()

# 绘制原始数据
plt.figure(figsize=(15, 6))
plt.subplot(211)
plt.plot(data["timestamp"], data["water_temperature"], label="origin data")
plt.xlabel("time")
plt.ylabel("temp")
plt.title("yushu temp")
plt.legend()

# 绘制日均水温
plt.subplot(212)
plt.plot(pd.to_datetime(daily_avg_temp["date"]), daily_avg_temp["water_temperature"], label="day_tem", color="r")
plt.xlabel("time")
plt.ylabel("temp")
plt.title("yushu tem")
plt.legend()

plt.tight_layout()
plt.show()
