% 从TXT文件读取数据
load strain_data1003.txt;
df = strain_data1003;


len = length(df);

% 归一化
yuanshidata = df(1:len,2);
datazz = yuanshidata';
data = mapminmax(datazz,0,1);

figure;
plot((1:numel(data)),data);
xlabel("Time (mins)");
ylabel("Vertical Acceleration (nm/s^2)");
title("Maduo Earthquake Data");
grid on;

fs = 1/60;
ts = 1/fs;

[cfs,frq] = cwt(data,fs);

tms = (0:numel(data)-1)/fs;

figure;
subplot(2,1,1);
plot(tms,data);
title("Original Data");
xlabel("Time (mins)");
ylabel("Amplitude");

subplot(2,1,2);
imagesc(tms,frq,abs(cfs));
shading flat;
xlabel("Time (mins)");
ylabel("Frequency");
set(gca,"yscale","log");
colormap(jet);
colorbar;
