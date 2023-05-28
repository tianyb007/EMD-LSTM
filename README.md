# EMD-LSTM

代码仓库是根据论文《基于 LSTM 的地震前兆同化分析探索》论文产生的。

使用本仓库的代码可以实现对时间序列数据的分解，并且使用 LSTM 神经网络对时间序列数据进行预测。

在 EMD-LSTM 系统中，首先使用 EMD 算法将时间序列数据分解成若干个内在模式函数（Intrinsic Mode Function, IMF）和一个残余项。这些 IMF 分量和残余项包含了原始时间序列的大部分信息，而且每个 IMF 分量都可以被看作是一种特定的振动模式。

这种分解方法有两大优势：

**减小了训练的复杂性：**每个 IMF 分量都相对简单，其复杂性都远小于原始的时间序列。因此，可以分别对每个 IMF 分量使用 LSTM 进行预测，这比直接对整个复杂的时间序列使用 LSTM 进行预测要容易得多。

**降低了预测的难度：**由于每个 IMF 分量都表示了原始时间序列的一种特定振动模式，因此我们可以根据这个振动模式来进行预测。这比预测原始的时间序列要简单得多，因为原始的时间序列可能包含了多种不同的、相互交织的振动模式。

在对每个 IMF 分量进行预测后，我们再将预测的 IMF 分量和预测的残余项合并，就可以得到对原始时间序列的预测。

这种基于 EMD 的预处理方法，使得 EMD-LSTM 系统在预测时间序列时的性能，相比单独使用 LSTM，得到了显著的提升。

## EMD

其中有关于经验模态分解的源代码

## LSTM

其中有关于 LSTM 神经网络预测时间序列数据的代码，还有一些是训练过程中保存的已经训练好的神经网络，可以直接拿来使用。

## 时频分析

在这个文件夹下面是使用 matlab 源码，时频分析是在 matlab 中进行的。

## 预处理

包含归零等预处理流程

## 格式转换

下载的数据中是一个时间戳跟 1440 个数据点，我更熟悉一个时间戳后面一个数据点的格式，根据你自己个人的喜好进行使用。
