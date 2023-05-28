import os

data_file = "C:/Users/tian/Desktop/data/wateremd_hou.txt"
# 将处理后的数据写入新的 txt 文件
output_file = "C:/Users/tian/Desktop/data/wateremd_zong.txt"
# 读取 txt 文件
with open(data_file, "r") as file:
    lines = file.readlines()

# 删除前 312480 行数据
# lines = lines[312480:]
# lines = lines[13062:]
# lines = lines[37440:]
# lines = lines[14400:]
# 删除最后 3000 行数据
lines = lines[:-14400]
# lines = lines[:-119519]


with open(output_file, "w") as file:
    for line in lines:
        file.write(line)

print(f"数据已保存到：{os.path.abspath(output_file)}")
