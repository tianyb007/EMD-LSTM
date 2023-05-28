% 从TXT文件读取数据
load water2021.txt;
df = water2021;

len = length(df);

% 归一化
yuanshidata = df(1:len,2);
data = yuanshidata';
% data = mapminmax(data,0,1);
figure
plot((1:numel(data)),data)
xlabel("Time (mins)")
ylabel("Data")
title("Maduo Earthquake Data")
grid on

% figure
% fs = 1/60;
% ts = 1/fs;
% colorbar;
% len = length(data);
% cwt(data,fs)
% [cfs,frq] = cwt(data,fs);
% colormap("jet");
% % clim([0.001,1]);