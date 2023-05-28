% Read data
data_file = 'C:/Users/tian/Desktop/data/2013_mod.txt';
data_table = readtable(data_file, 'Delimiter', ' ', 'ReadVariableNames', false);

% Initialize empty data array
data = [];

% Process each row of data
% Process each row of data
for i = 1:height(data_table)
    date = data_table{i, 1};
    values_cell = table2cell(data_table(i, 2:end));
    values = cell2mat(values_cell);

    % Replace 999999 and values > 14 with NaN and add them to the data array
    for j = 1:length(values)
        value = values(j);
        if value == 999999 || value < 9.86 || value > 9.96
            value = NaN;
        end
        date_str = datestr(date, 'yyyy-mm-dd');
        timestamp = datetime(date_str, 'InputFormat', 'yyyy-MM-dd') + minutes(j-1);
        timestamp.Format = 'yyyy-MM-dd HH:mm';
        data = [data; {timestamp, value}];
    end
end

% Convert the data cell array to a timetable
data_tt = cell2table(data, 'VariableNames', {'timestamp', 'water_temperature'});



% Convert data to timetable
data_timetable = array2timetable(data, 'VariableNames', {'WaterTemperature'}, 'RowTimes', data(:, 1));

% Sort the data by timestamp
data_timetable = sortrows(data_timetable);

% Linearly interpolate missing values
data_timetable.WaterTemperature = fillmissing(data_timetable.WaterTemperature, 'linear');

% Visualize the processed data
figure
plot(data_timetable.Time, data_timetable.WaterTemperature, 'k', 'LineWidth', 0.5)
xlabel('Date')
ylabel('Water Temperature')
title('Water Temperature Data 2013')
datetick('x', 'yyyy-mm-dd')

% CWT calculation
sampling_period = 1; % 1-minute sampling period
signal = data_timetable.WaterTemperature;
time_points = (1:length(signal)) * sampling_period;

wavelet = 'cmor1.5-1.0'; % You can try other wavelets like 'morl', 'cgau5', etc.
scales = 1:100; % Adjust scales range for finer or coarser time-frequency representation
cwt_coefficients = cwt(signal, scales, wavelet, sampling_period);

% Time-frequency plot
figure
imagesc(time_points, scales, abs(cwt_coefficients))
colormap('viridis')
colorbar('Label', 'Magnitude')
xlabel('Time (minutes)')
ylabel('Scale')
title('CWT Time-Frequency Representation')
axis tight
