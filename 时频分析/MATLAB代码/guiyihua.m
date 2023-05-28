% 从TXT文件读取数据
filename = 'C:/Users/tian/Documents/MATLAB/zero/zuankong/strain_data1003.txt';
data = dlmread(filename);

% 提取时间戳和应变数据
timestamps = data(:, 1);
strain_data = data(:, 2);

% 将时间戳转换为字符串，以便后续处理
timestamps_str = cellstr(num2str(timestamps, '%.0f'));

% 将时间戳字符串转换为datenum格式
time_datenum = datenum(timestamps_str, 'yyyyMMddHHmm');

% 计算时间间隔（单位：分钟）
time_minutes = (time_datenum - time_datenum(1)) * 24 * 60;

% 采样频率（每分钟一次采样）
fs = 1/60;

% 数据长度
N = length(strain_data);

% 消除直流分量
strain_data = strain_data - mean(strain_data);

% 消除线性趋势
strain_data = detrend(strain_data);

% 设计带通滤波器（例如保留 0.0001 Hz 到 0.008 Hz 的频率）
filter_order = 4;
low_freq = 0.0001;
high_freq = 0.008;
[b, a] = butter(filter_order, [low_freq, high_freq] / (fs/2), 'bandpass');

% 应用滤波器
strain_data_filtered = filtfilt(b, a, strain_data);

% 选择窗口长度（例如10分钟）
window_length = 10 * fs;
window = hamming(window_length);

% 计算STFT
[S, F, T] = spectrogram(strain_data_filtered, window, [], [], fs, 'yaxis');

% 计算功率谱密度（PSD）
PSD = 10 * log10(abs(S).^2);

% 归一化PSD
PSD_normalized = (PSD - min(PSD(:))) / (max(PSD(:)) - min(PSD(:)));

% 绘制时频图
figure;
surf(T, F, PSD_normalized, 'EdgeColor', 'none');
axis xy;
view(0, 90);
xlabel('Time (minutes)');
ylabel('Frequency (Hz)');
title('Short-Time Fourier Transform (STFT)');
colorbar;
