% 用短时傅里叶变换做的时频图
% 读取数据文件
filename = 'strain_data1003.txt';
data = dlmread(filename);

% 转换时间戳为日期时间格式
timestamps = data(:,1);
dates = datetime(num2str(timestamps),'InputFormat','yyyyMMddHHmm');

% 获取数据值
values = data(:,2);
% 消除直流分量
values = values - mean(values);

% 消除线性趋势
values = detrend(values);
% 绘制图形
figure;
plot(dates, values);
xlabel('Time');
ylabel('Values');
title('Time Series Visualization');
grid on;
% 三次样条插值以提高采样率
old_fs = 1/60; % 原始采样率
new_fs = 1; % 新采样率
% old_time = (0:length(values)-1) * old_fs;
% new_time = (0:(length(values)-1)*new_fs/old_fs) * old_fs;
% new_values = interp1(old_time, values, new_time, 'spline');
% figure;
% plot(dates, values);
% xlabel('new_time');
% ylabel('new_values');
% title('Time Series Visualization');
% grid on;

% 将插值后的数据保存到本地文件
% interpolated_data = [new_time', new_values];
% writematrix(interpolated_data, 'interpolated_data.csv');

values = mapminmax(values,0,1);
% 设置STFT参数
window = 256; % 窗口大小
noverlap = 128; % 重叠大小
nfft = 512; % FFT点数

% 计算STFT
[s, f, t] = spectrogram(values, window, noverlap, nfft, fs);

% 绘制频谱图
figure;
imagesc(t, f, 20*log10(abs(s))); % 用dB单位绘制
axis xy;
xlabel('Time (s)');
ylabel('Frequency (Hz)');
title('Spectrogram');
colorbar;