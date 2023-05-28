% 从TXT文件读取数据
% filename = 'C:/Users/tian/Documents/MATLAB/zero/zuankong/strain_data_1003.txt'; % 替换为你的数据文件名

% 从TXT文件读取数据
% 从TXT文件读取数据
filename = 'strain_data1003.txt'; % 替换为你的数据文件名
data = dlmread(filename);

% 提取时间戳和应变数据
timestamps = data(:, 1);
strain_data = data(:, 2);

% 将时间戳转换为字符串，以便后续处理
timestamps_str = cellstr(num2str(timestamps, '%.0f'));

% 将时间戳字符串转换为datenum格式
time_datenum = datenum(timestamps_str, 'yyyyMMddHHmm');

% 检查并删除重复的时间点
[time_datenum, unique_indices] = unique(time_datenum);
strain_data = strain_data(unique_indices);

% 计算时间间隔（单位：分钟）
original_time = (time_datenum - time_datenum(1)) * 24 * 60;

% 采样频率（每分钟一次采样）
fs = 1/60;

% 插值后的时间向量
interpolated_time = 0:1/60:(length(strain_data))*(1/60);

% 为了避免越界，我们需要在插值后的时间向量中删除最后一个元素
interpolated_time(end) = [];

% 使用三次样条插值将数据插值到1 Hz
strain_data_interpolated = interp1(original_time, strain_data, interpolated_time, 'spline');

% 更新采样频率
fs = 1;

% 绘制原始数据
figure;
plot(original_time, strain_data);
xlabel('Time (minutes)');
ylabel('Strain');
title('Original Strain Data');

% 绘制插值后的数据
figure;
plot(interpolated_time, strain_data_interpolated);
xlabel('Time (minutes)');
ylabel('Strain');
title('Interpolated Strain Data (1 Hz)');


% 滤波处理
fs = 1; % 采样频率（Hz）
low_freq = 0.001; % 低频截止频率（Hz）
high_freq = 0.5; % 高频截止频率（保留能保留的最高频率）
filter_order = 4; % 滤波器阶数

[b, a] = butter(filter_order, [low_freq, high_freq] / (fs / 2), 'bandpass');
strain_data_filtered = filtfilt(b, a, strain_data_interpolated);

% 连续小波变换
mother_wavelet = 'morl'; % 使用Morlet母小波
scales = 1:200; % 尺度范围，可以根据需要进行调整
[cfs, frequencies] = cwt(strain_data_filtered, scales, mother_wavelet, 1/fs);

% 绘制连续小波变换结果
figure;
surface(interpolated_time, frequencies, abs(cfs));
shading interp;
axis tight;
xlabel('Time (minutes)');
ylabel('Frequency (Hz)');
title('CWT of Filtered Strain Data');
colorbar;
