import numpy as np
from scipy.signal import butter, lfilter

# 设计带通滤波器
def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

# 应用滤波器
def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

# 假设采样频率是1000Hz
fs = 1000.0
# 规定滤波频率为0.2-0.5Hz
lowcut = 0.2
highcut = 0.5
# 采样2500个数据点
t = np.linspace(0, 1.0, 2500, endpoint=False)
# 生成一个正弦波信号，频率为10Hz，加上0.5的高斯噪声
signal = np.sin(10.0 * 2.0*np.pi*t) + 0.5*np.random.randn(len(t))
# 应用带通滤波器
y = butter_bandpass_filter(signal, lowcut, highcut, fs, order=2)


import matplotlib.pyplot as plt

# 绘制信号的时域图和频谱图
plt.figure(figsize=[12, 6])
plt.subplot(1, 2, 1)
plt.plot(t, signal, 'b-', label='data')
plt.plot(t, y, 'g-', linewidth=2, label='filtered data')
plt.xlabel('Time [sec]')
plt.grid()
plt.legend()

plt.subplot(1, 2, 2)
N = len(signal)
Y = np.fft.fft(signal)/N
Y = 2*np.abs(Y[:N//2])
freq = np.linspace(0, fs/2, len(Y))
plt.plot(freq, Y, 'b-', label='data')

N = len(y)
Y = np.fft.fft(y)/N
Y = 2*np.abs(Y[:N//2])
freq = np.linspace(0, fs/2, len(Y))
plt.plot(freq, Y, 'g-', linewidth=2, label='filtered data')
plt.xlabel('Frequency [Hz]')
plt.grid()
plt.legend()

plt.show()

