# Keras-LSTM.py

# 简介：Keras中带LSTM的多变量时间序列预测
# 像long short-term memory递归神经网络这样的神经网络几乎可以完美的模拟多个输入变量的问题。
# 这在时间序列预测中是一个很大的好处，经典的线性方法很难适应
# 在本教程中，您将了解如何在keras深度学习库中开发用于多变量时间序列预测的LSTM模型。
# 完成本教程后将知道：
# 1.如何将原始数据集转换为我们可用于时间序列预测的东西
# 2.如何准备数据和将一个LSTM模型拟合到一个多变量的时间序列预测问题上
# 3.如何进行预测并将结果重新调整到原始单位





# 分为三个部分
# 空气污染预测
# 基本数据准备
# 多变量LSTM预测模型


# 1.空气污染预测
# 在本教程中将使用空气质量数据集
# 这是一个报告了中国北京美国大使馆五年每个小时的天气和污染程度的数据集。
# 这些数据包括日期时间，称为PM2.5浓度的污染以及包括露点，温度，压力，风向，风速和累计雨雪小时数在内的天气信息。原始数据中的完整功能列表如下：
# No：行号
# year：这一行中的数据年份
# month：此行中的数据月份
# day：这一行中的数据日
# hour：此行中的小时数据
# pm2.5：PM2.5浓度
# DEWP：露点
# TEMP：温度
# PRES：压力
# cbwd：综合风向
# Iws：累计风速
# Is：累积下了几个小时的雪
# Ir：累积下了几个小时的雨

# 我们可以使用这些数据，并构建一个预测问题，在前一天的天气条件和污染情况下，我们预测下一个小时的污染情况。
# url:https://archive.ics.uci.edu/ml/datasets/Beijing+PM2.5+Data
# 下载数据集并将其放在当前工作目录中，文件名为 “ raw.csv ”。


# 基本数据准备
# 数据尚未准备好使用，我们必须先准备。
# 以下是原始数据集的前几行。
No,year,month,day,hour,pm2.5,DEWP,TEMP,PRES,cbwd,Iws,Is,I
1,2010,1,1,0,NA,-21,-11,1021,NW,1.79,0,0
2,2010,1,1,1,NA,-21,-12,1020,NW,4.92,0,0
3,2010,1,1,2,NA,-21,-11,1019,NW,6.71,0,0
4,2010,1,1,3,NA,-21,-14,1019,NW,9.84,0,0
5,2010,1,1,4,NA,-20,-12,1018,NW,12.97,0,0

# 第一步是将日期-时间信息合并成一个日期-时间，以便我们可以将它用作pandas的一个索引。
# 快速检查显示前24小时pm2.5的na值。因此我们将需要删除第一行数据。数据集中后面还有一些零散的NA值，我们用0来标记它们。
# 
# 下面的脚本加载原始数据集，并将日期-时间信息解析为pandas dataframe索引。“否”列被删除，然后为每列指定更清晰的名称。最后，将NA值替换为0，并将前24小时删除。
from pandas import read_csv
from datetime import datetime
# 加载数据
def parse(x):
    return datetime.strptime(x, '%Y %m %d %H')
dataset = read_csv('raw.csv',  parse_dates = [['year', 'month', 'day', 'hour']], index_col=0, date_parser=parse)
dataset.drop('No', axis=1, inplace=True)
# 手动更改列名
dataset.columns = ['pollution', 'dew', 'temp', 'press', 'wnd_dir', 'wnd_spd', 'snow', 'rain']
dataset.index.name = 'date'
# 把所有NA值用0替换
dataset['pollution'].fillna(0, inplace=True)
# 丢弃前24小时
dataset = dataset[24:] 
# 输出前五行
print(dataset.head(5))
# 保存到文件中
dataset.to_csv('pollution.csv')
# 运行该示例将输出转换数据集的前5行，并将数据集保存为“ pollution.csv ”。
                     pollution  dew  temp   press wnd_dir  wnd_spd  snow  rain
date
2010-01-02 00:00:00      129.0  -16  -4.0  1020.0      SE     1.79     0     0
2010-01-02 01:00:00      148.0  -15  -4.0  1020.0      SE     2.68     0     0
2010-01-02 02:00:00      159.0  -11  -5.0  1021.0      SE     3.57     0     0
2010-01-02 03:00:00      181.0   -7  -5.0  1022.0      SE     5.36     1     0
2010-01-02 04:00:00      138.0   -7  -5.0  1022.0      SE     6.25     2     0
# 现在我们有了一个易于使用的数据形式，我们可以快速绘制每个系列的图，看看我们有什么。
# 下面的代码加载新的“ pollution.csv ”文件，并将每个序列作为一个单独的子图绘制，除了风速dir（这是绝对的）之外。
from pandas import read_csv
from matplotlib import pyplot
# 加载数据集
dataset = read_csv('pollution.csv', header=0, index_col=0)
values = dataset.values
# 指定要绘制的列
groups = [0, 1, 2, 3, 5, 6, 7]
i = 1
# 绘制每一列
pyplot.figure()
for group in groups:
    pyplot.subplot(len(groups), 1, i)
    pyplot.plot(values[:, group])
    pyplot.title(dataset.columns[group], y=0.5, loc='right')
    i += 1
pyplot.show()
# 运行该示例绘制了一个包含7个子图的图，显示了每个变量的5年数据。


# 多元LSTM预测模型
# 在本节中，我们将选择适合LSTM的问题
# LSTM数据准备
# 第一步是准备LSTM的污染数据集
# 这涉及到将数据集构造为监督学习问题 & 对输入变量进行归一化
# 我们将监督学习问题的框架，作为污染测量和天气条件在前一个时间步骤(t)预测污染

# 首先，加载“ pollution.csv ”数据集。风速特征是标签编码（整数编码）。如果你有兴趣探索它，这可能会进一步在未来编码。
# 接下来，将所有特征归一化，然后将该数据集变换成监督学习问题。然后去除要预测小时的天气变量（t）。
# 下面提供了完整的代码清单。

# 将序列转换成监督学习问题
def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
    n_vars = 1 if type(data) is list else data.shape[1]
    df = DataFrame(data)
    cols, names = list(), list()
    # input sequence (t-n, ... t-1)
    for i in range(n_in, 0, -1):
        cols.append(df.shift(i))
        names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
    # forecast sequence (t, t+1, ... t+n)
    for i in range(0, n_out):
        cols.append(df.shift(-i))
        if i == 0:
            names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
        else:
            names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
    # put it all together
    agg = concat(cols, axis=1)
    agg.columns = names
    # drop rows with NaN values
    if dropnan:
        agg.dropna(inplace=True)
    return agg
 
# 加载数据集
dataset = read_csv('pollution.csv', header=0, index_col=0)
values = dataset.values
# 整数编码方向
encoder = LabelEncoder()
values[:,4] = encoder.fit_transform(values[:,4])
# 确保所有数据是浮动的
values = values.astype('float32')
# 归一化特征
scaler = MinMaxScaler(feature_range=(0, 1))
scaled = scaler.fit_transform(values)
# 构建成监督学习问题
reframed = series_to_supervised(scaled, 1, 1)
# 丢弃我们不想预测的列
reframed.drop(reframed.columns[[9,10,11,12,13,14,15]], axis=1, inplace=True)
print(reframed.head())

# 运行该示例将打印转换数据集的前5行。我们可以看到8个输入变量（输入序列）和1个输出变量（当前小时的污染程度）。
   var1(t-1)  var2(t-1)  var3(t-1)  var4(t-1)  var5(t-1)  var6(t-1)  \
1   0.129779   0.352941   0.245902   0.527273   0.666667   0.002290
2   0.148893   0.367647   0.245902   0.527273   0.666667   0.003811
3   0.159960   0.426471   0.229508   0.545454   0.666667   0.005332
4   0.182093   0.485294   0.229508   0.563637   0.666667   0.008391
5   0.138833   0.485294   0.229508   0.563637   0.666667   0.009912
 
   var7(t-1)  var8(t-1)   var1(t)
1   0.000000        0.0  0.148893
2   0.000000        0.0  0.159960
3   0.000000        0.0  0.182093
4   0.037037        0.0  0.138833
5   0.074074        0.0  0.109658


# 定义和拟合模型
# 在本节中，我们将在多元输入数据上拟合一个LSTM模型。

# 首先，我们必须将准备好的数据集分解为训练集和测试集。为了加速演示中对模型的训练，我们将只适合第一年的数据模型，然后在剩下的4年数据上进行评估。如果有时间的话，可以考虑探索这个测试工具的倒置版本。
# 下面的例子将数据集分解为训练集和测试集，然后将训练集和测试集分解为输入和输出变量。最后，输入（X）重塑成LSTM预期的3D格式，即[样例，时间步，特征]。
# 把数据分为训练集和测试集
values = reframed.values
n_train_hours = 365 * 24
train = values[:n_train_hours, :]
test = values[n_train_hours:, :]
# 把数据分为输入和输出
train_X, train_y = train[:, :-1], train[:, -1]
test_X, test_y = test[:, :-1], test[:, -1]
# 把输入重塑成3D格式 [样例， 时间步, 特征]
train_X = train_X.reshape((train_X.shape[0], 1, train_X.shape[1]))
test_X = test_X.reshape((test_X.shape[0], 1, test_X.shape[1]))
# 运行此示例将输出训练集和测试集的输入输出形状，其中包含大约9K小时的训练数据和大约35K小时的测试数据。
print(train_X.shape, train_y.shape, test_X.shape, test_y.shape)
(8760, 1, 8) (8760,) (35039, 1, 8) (35039,)

# 现在我们可以定义和拟合我们的LSTM模型。
# 我们将在第一隐层中定义50个神经元，在输出层中定义1个神经元用于预测污染。输入形状将是带有8个特征的一个时间步。
# 我们将使用平均绝对误差（MAE）损失函数和随机梯度下降的高效Adam版本。
# 该模型将适用于批量大小为72的50个训练时期。请记住，Keras中的LSTM的内部状态在每个批次结束时被重置，所以是多天函数的内部状态可能是有用的（尝试测试）。
# 最后，我们通过在fit（）函数中设置validation_data参数来跟踪训练期间的训练和测试损失。在运行结束时，训练和测试损失都被绘制出来。

# 设计网络
model = Sequential()
model.add(LSTM(50, input_shape=(train_X.shape[1], train_X.shape[2])))
model.add(Dense(1))
model.compile(loss='mae', optimizer='adam')
# 拟合网络
history = model.fit(train_X, train_y, epochs=50, batch_size=72, validation_data=(test_X, test_y), verbose=2, shuffle=False)
# 绘制历史数据
pyplot.plot(history.history['loss'], label='train')
pyplot.plot(history.history['val_loss'], label='test')
pyplot.legend()
pyplot.show()

# 评估模型
# 模型拟合后，我们可以预测整个测试数据集。
# 我们将预测与测试数据集结合起来，并将缩放比例倒置。我们还将测试数据集与预期的污染数据进行了转换。
# 通过预测值和实际值，我们可以计算模型的误差分数。在这种情况下，我们计算出与变量本身相同的单位给出误差的均方根误差（RMSE）。

# 作出预测
yhat = model.predict(test_X)
test_X = test_X.reshape((test_X.shape[0], test_X.shape[2]))
# 反向缩放预测值
inv_yhat = concatenate((yhat, test_X[:, 1:]), axis=1)
inv_yhat = scaler.inverse_transform(inv_yhat)
inv_yhat = inv_yhat[:,0]
# 反向缩放实际值
test_y = test_y.reshape((len(test_y), 1))
inv_y = concatenate((test_y, test_X[:, 1:]), axis=1)
inv_y = scaler.inverse_transform(inv_y)
inv_y = inv_y[:,0]
# 计算RMSE
rmse = sqrt(mean_squared_error(inv_y, inv_yhat))
print('Test RMSE: %.3f' % rmse)

# 完整例子
# 完整的例子如下所示。
# 注意：这个例子假定你已经准备好了正确的数据，例如把下载的“ raw.csv ”转换成准备好的“ pollution.csv ”。

from math import sqrt
from numpy import concatenate
from matplotlib import pyplot
from pandas import read_csv
from pandas import DataFrame
from pandas import concat
from sklearn.preprocessing import MinMaxScale
from sklearn.preprocessing import LabelEncode
from sklearn.metrics import mean_squared_erro
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
 
# 转换序列成监督学习问题
def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
    n_vars = 1 if type(data) is list else data.shape[1]
    df = DataFrame(data)
    cols, names = list(), list()
    # input sequence (t-n, ... t-1)
    for i in range(n_in, 0, -1):
        cols.append(df.shift(i))
        names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
    # forecast sequence (t, t+1, ... t+n)
    for i in range(0, n_out):
        cols.append(df.shift(-i))
        if i == 0:
            names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
        else:
            names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
    # put it all together
    agg = concat(cols, axis=1)
    agg.columns = names
    # drop rows with NaN values
    if dropnan:
        agg.dropna(inplace=True)
    return agg
 
# 加载数据集
dataset = read_csv('pollution.csv', header=0, index_col=0)
values = dataset.values
# 整数编码
encoder = LabelEncoder()
values[:,4] = encoder.fit_transform(values[:,4])
# ensure all data is float
values = values.astype('float32')
# 归一化特征
scaler = MinMaxScaler(feature_range=(0, 1))
scaled = scaler.fit_transform(values)
# 构建监督学习问题
reframed = series_to_supervised(scaled, 1, 1)
# 丢弃我们并不想预测的列
reframed.drop(reframed.columns[[9,10,11,12,13,14,15]], axis=1, inplace=True)
print(reframed.head())
 
# 分割为训练集和测试集
values = reframed.values
n_train_hours = 365 * 24
train = values[:n_train_hours, :]
test = values[n_train_hours:, :]
# 分为输入输出
train_X, train_y = train[:, :-1], train[:, -1]
test_X, test_y = test[:, :-1], test[:, -1]
# 重塑成3D形状 [样例, 时间步, 特征]
train_X = train_X.reshape((train_X.shape[0], 1, train_X.shape[1]))
test_X = test_X.reshape((test_X.shape[0], 1, test_X.shape[1]))
print(train_X.shape, train_y.shape, test_X.shape, test_y.shape)
 
# 设计网络
model = Sequential()
model.add(LSTM(50, input_shape=(train_X.shape[1], train_X.shape[2])))
model.add(Dense(1))
model.compile(loss='mae', optimizer='adam')
# 拟合神经网络模型
history = model.fit(train_X, train_y, epochs=50, batch_size=72, validation_data=(test_X, test_y), verbose=2, shuffle=False)
# 绘制历史数据
pyplot.plot(history.history['loss'], label='train')
pyplot.plot(history.history['val_loss'], label='test')
pyplot.legend()
pyplot.show()
 
# 做出预测
yhat = model.predict(test_X)
test_X = test_X.reshape((test_X.shape[0], test_X.shape[2]))
# 反向转换预测值比例
inv_yhat = concatenate((yhat, test_X[:, 1:]), axis=1)
inv_yhat = scaler.inverse_transform(inv_yhat)
inv_yhat = inv_yhat[:,0]
# 反向转换实际值比例
test_y = test_y.reshape((len(test_y), 1))
inv_y = concatenate((test_y, test_X[:, 1:]), axis=1)
inv_y = scaler.inverse_transform(inv_y)
inv_y = inv_y[:,0]
# 计算RMSE
rmse = sqrt(mean_squared_error(inv_y, inv_yhat))
print('Test RMSE: %.3f' % rmse)

# 首先运行示例创建一个显示训练期间训练集和测试集损失的图表。
# 我们可以看到测试损失低于训练损失。该模型可能过度拟合。在训练过程中测量和绘制均方根误差可能会使我们看到更多的信息。
# 训练和测试损失被输出在每个训练时期结束时。在运行结束时，打印测试数据集上模型的最终RMSE。
# 我们可以看到，该模型达到了26.496的可比RMSE，低于用持久性模型发现的RMSE30。
# ...
Epoch 46/50
0s - loss: 0.0143 - val_loss: 0.0133
Epoch 47/50
0s - loss: 0.0143 - val_loss: 0.0133
Epoch 48/50
0s - loss: 0.0144 - val_loss: 0.0133
Epoch 49/50
0s - loss: 0.0143 - val_loss: 0.0133
Epoch 50/50
0s - loss: 0.0144 - val_loss: 0.0133
Test RMSE: 26.496

# 关于如何调整上面的示例以在多个以前的时间步骤中训练模型，已经有许多请求。
# 在写这篇文章的时候，我尝试了这个和其他许多配置，并决定不包含它们，因为它们没有提升模型。
# 不过，我已经把下面这个例子作为参考模板，可以适应自己的问题。
# 在以前的多个时间步中训练模型所需的更改非常少，如下所示：
# 首先，调用series_to_supervised（）时，必须适当地构造问题。我们将使用3小时的数据作为输入。另请注意，我们不再明确地删除ob（t）中所有其他字段的列。

# 为滞后小时指定大小
n_hours = 3
n_features = 8
# frame as supervised learning
reframed = series_to_supervised(scaled, n_hours, 1)

# 接下来，我们需要更加小心地指定输入和输出的列。
# 我们在框架数据集中有3 * 8 + 8列。我们会将3 * 8或24列作为前3小时所有功能的输入。我们将在下一小时将污染变量作为输出，如下所示：
# 分为输入和输出
n_obs = n_hours * n_features
train_X, train_y = train[:, :n_obs], train[:, -n_features]
test_X, test_y = test[:, :n_obs], test[:, -n_features]
print(train_X.shape, len(train_X), train_y.shape)1
# 接下来，我们可以正确地重塑我们的输入数据，以反映时间步骤和功能。
# 重塑成3D格式 [samples, timesteps, features]
train_X = train_X.reshape((train_X.shape[0], n_hours, n_features))
test_X = test_X.reshape((test_X.shape[0], n_hours, n_features))
# 拟合模型是一样的。
# 唯一的另一个小变化就是如何评估模型。具体而言，在我们如何重构具有8列的行适合于反转缩放操作以将y和y返回到原始尺度以便我们可以计算RMSE。
# 改变的要点是我们将y或yhat列与测试数据集的最后7个特征连接起来，以反比例缩放，如下所示：
# 反向缩放预测值
inv_yhat = concatenate((yhat, test_X[:, -7:]), axis=1)
inv_yhat = scaler.inverse_transform(inv_yhat)
inv_yhat = inv_yhat[:,0]
# 反向缩放实际值
test_y = test_y.reshape((len(test_y), 1))
inv_y = concatenate((test_y, test_X[:, -7:]), axis=1)
inv_y = scaler.inverse_transform(inv_y)
inv_y = inv_y[:,0]

# 我们可以将所有这些修改与上面的例子结合在一起。具有多滞后输入的多变量时间序列预测的完整示例如下所示：
# from math import sqrt
from numpy import concatenate
from matplotlib import pyplot
from pandas import read_csv
from pandas import DataFrame
from pandas import concat
from sklearn.preprocessing import MinMaxScale
from sklearn.preprocessing import LabelEncode
from sklearn.metrics import mean_squared_erro
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
 
# 将序列转换为监督学习问题
def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
    n_vars = 1 if type(data) is list else data.shape[1]
    df = DataFrame(data)
    cols, names = list(), list()
    # input sequence (t-n, ... t-1)
    for i in range(n_in, 0, -1):
        cols.append(df.shift(i))
        names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
    # forecast sequence (t, t+1, ... t+n)
    for i in range(0, n_out):
        cols.append(df.shift(-i))
        if i == 0:
            names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
        else:
            names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
    # put it all togethe
    agg = concat(cols, axis=1)
    agg.columns = names
    # drop rows with NaN values
    if dropnan:
        agg.dropna(inplace=True)
    return agg
 
# 加载数据集
dataset = read_csv('pollution.csv', header=0, index_col=0)
values = dataset.values
# 整数编码
encoder = LabelEncoder()
values[:,4] = encoder.fit_transform(values[:,4])
# 确保所有数据是浮动的
values = values.astype('float32')
# 归一化特征
scaler = MinMaxScaler(feature_range=(0, 1))
scaled = scaler.fit_transform(values)
# 指定滞后时间大小
n_hours = 3
n_features = 8
# 构建监督学习问题
reframed = series_to_supervised(scaled, n_hours, 1)
print(reframed.shape)
 
# 分为训练集和测试集
values = reframed.values
n_train_hours = 365 * 24
train = values[:n_train_hours, :]
test = values[n_train_hours:, :]
# 分为输入和输出
n_obs = n_hours * n_features
train_X, train_y = train[:, :n_obs], train[:, -n_features]
test_X, test_y = test[:, :n_obs], test[:, -n_features]
print(train_X.shape, len(train_X), train_y.shape)
# 重塑为3D形状 [samples, timesteps, features]
train_X = train_X.reshape((train_X.shape[0], n_hours, n_features))
test_X = test_X.reshape((test_X.shape[0], n_hours, n_features))
print(train_X.shape, train_y.shape, test_X.shape, test_y.shape)
 
# 设计网络
model = Sequential()
model.add(LSTM(50, input_shape=(train_X.shape[1], train_X.shape[2])))
model.add(Dense(1))
model.compile(loss='mae', optimizer='adam')
# 拟合网络模型
history = model.fit(train_X, train_y, epochs=50, batch_size=72, validation_data=(test_X, test_y), verbose=2, shuffle=False)
# 绘制历史数据
pyplot.plot(history.history['loss'], label='train')
pyplot.plot(history.history['val_loss'], label='test')
pyplot.legend()
pyplot.show()
 
# 作出预测
yhat = model.predict(test_X)
test_X = test_X.reshape((test_X.shape[0], n_hours*n_features))
# 反向转换预测值比例
inv_yhat = concatenate((yhat, test_X[:, -7:]), axis=1)
inv_yhat = scaler.inverse_transform(inv_yhat)
inv_yhat = inv_yhat[:,0]
# 反向转换实际值大小
test_y = test_y.reshape((len(test_y), 1))
inv_y = concatenate((test_y, test_X[:, -7:]), axis=1)
inv_y = scaler.inverse_transform(inv_y)
inv_y = inv_y[:,0]
# 计算RMSE大小
rmse = sqrt(mean_squared_error(inv_y, inv_yhat))
print('Test RMSE: %.3f' % rmse)

# 我会补充说，LSTM 似乎不适合自回归类型的问题，并且您可能更适合用大窗口探索MLP。
# 我希望这个例子可以帮助你进行自己的时间序列预测实验。
# 自回归模型（英语：Autoregressive model，简称AR模型），是统计上一种处理时间序列的方法，用同一变数例如x的之前各期，亦即x1至xt-1来预测本期xt的表现，并假设它们为一线性关系。因为这是从回归分析中的线性回归发展而来，只是不用x预测y，而是用x预测 x（自己）；所以叫做自回归。