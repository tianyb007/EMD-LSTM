import pandas as pd
import matplotlib.pyplot as plt

# 读取数据
data_file = "C:/Users/tian/Desktop/data/wateremd.txt"
df = pd.read_csv(data_file, delimiter=' ', names=["timestamp", "value"])

# 将字符串格式的时间戳转换为 pandas.Timestamp
df["timestamp"] = pd.to_datetime(df["timestamp"], format="%Y%m%d%H%M")

# 绘制数据
plt.figure(figsize=(18, 9))
plt.plot(df["timestamp"], df["value"], color="black", linewidth=0.5, linestyle="solid")
plt.xlabel("Date")
plt.ylabel("Value")
plt.title("Data Visualization")
plt.grid()
plt.show()
