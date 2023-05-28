% 从TXT文件读取数据
load water.txt;
df = water;
% load zuankong.txt;
% df = zuankong;
% load NW.txt;
% df = NW;
len = length(df);

% 归一化
yuanshidata = df(1:len,2);
data = yuanshidata';
% data = mapminmax(data,0,1);

figure
plot((1:numel(data)),data,'black')
xlabel("Time")
ylabel("Data")
% title("Maduo Earthquake Data")
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