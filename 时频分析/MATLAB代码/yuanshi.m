% 从TXT文件读取数据
load strain_data1003.txt;
df = strain_data1003;

nrow = length(df);

% 归一化
yuanshidata = df(1:nrow,2);
datazz = yuanshidata';
data = mapminmax(datazz,0,1);
figure
plot((1:numel(data)),data)
xlabel("Time (mins)")
ylabel("Data")
title("Maduo Earthquake Data")
grid on
figure
fs = 1/60;
ts = 1/fs;
colorbar;
len = length(data);
cwt(data,fs)
[cfs,frq] = cwt(data,fs);
colormap("jet");


