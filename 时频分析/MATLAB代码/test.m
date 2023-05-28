% 从TXT文件读取数据
filename = 'C:/Users/tian/Documents/MATLAB/zero/zuankong/strain_data.txt';
data = importdata(filename);

% 提取时间戳和应变数据
timestamps = data.textdata;
strain_data = data.data;

% 将时间戳转换为datenum格式，以便后续处理
time_datenum = datenum(timestamps, 'yyyymmddHHMM');

% 计算时间间隔（单位：分钟）
time_minutes = (time_datenum - time_datenum(1)) * 24 * 60;

% 采样频率（每分钟一次采样）
fs = 1/60;

% 数据长度
N = length(strain_data);

% 选择窗口长度（例如10分钟）
window_length = 10 * fs;
window = hamming(window_length);

% 计算STFT
[S, F, T] = spectrogram(strain_data, window, [], [], fs, 'yaxis');

% 计算功率谱密度（PSD）
PSD = 10 * log10(abs(S).^2);

% 绘制时频图
figure;
surf(T, F, PSD, 'EdgeColor', 'none');
axis xy;
view(0, 90);
xlabel('Time (minutes)');
ylabel('Frequency (Hz)');
title('Short-Time Fourier Transform (STFT)');
colorbar;
