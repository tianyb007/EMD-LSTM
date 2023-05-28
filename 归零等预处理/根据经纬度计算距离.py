from math import asin, cos, pi, radians, sin, sqrt

# Haversine公式
lat1, lon1 = 31.93, 92.86
# 玉树地震台位置
lat2, lon2 = 32.56, 96.91
r = 6371  # 地球平均半径,单位km

lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

dlat = lat2 - lat1
dlon = lon2 - lon1

a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
c = 2 * asin(sqrt(a))

distance = r * c
print(f'两地距离为:{distance} km')
# 纳什维尔到洛杉矶的距离为:2889.16 km
