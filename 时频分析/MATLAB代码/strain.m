% 读取数据
data_file = 'strain2010.CSV';

% 从csv文件中读取数据
df = readtable(data_file, 'Delimiter', ',', 'ReadVariableNames', false);

len = height(df);

% 归一化
yuanshidata = df{1:len, 2};
datazz = yuanshidata';
data = mapminmax(datazz, 0, 1);

% 查找非空缺值
non_missing_indices = ~isnan(data);
x_non_missing = find(non_missing_indices);
y_non_missing = data(non_missing_indices);

% 对空缺值进行插值
x_full = 1:numel(data);
data_interpolated = interp1(x_non_missing, y_non_missing, x_full, 'linear');

figure;
plot((1:numel(data_interpolated)), data_interpolated);
xlabel("Time (mins)");
ylabel("Vertical Acceleration (nm/s^2)");
title("Maduo Earthquake Data");
grid on;

fs = 1/60;
ts = 1/fs;

[cfs, frq] = cwt(data_interpolated, fs);
figure
imagesc((1:numel(data_interpolated)), frq, abs(cfs));
xlabel("Time (mins)");
ylabel("Frequency");
set(gca, "yscale", "log");
colormap(jet);
colorbar;
