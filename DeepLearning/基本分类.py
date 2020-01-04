# 训练首个神经网络：基本分类

# 本指南会训练一个对服饰（例如运动鞋和衬衫）图像进行分类的神经网络模型。
# 本教程只是简要介绍一个完整的tensorflow程序
# 本教程使用的是tf.keras，它是一种用于在tensorflow中构建和训练模型的高阶API


# tensorflow & tf.keras
import tensorflow as tf
from tensorflow import keras

# Helper libraries
import numpy as np
import matplotlib.pyplot as plt

print(tf.__version__)

# 导入fashion mnist数据集

# 本指南使用fashion mnist数据集，其中包含70000张灰度图像，涵盖10个类别。
# fashion mnist的作用是成为经典MNIST数据集的简易替换，后者通常用作计算机视觉机器学习程序的
# ”hello,world"入门数据集，mnist数据集包含手写数字（0、1、2等）的图像，这些图像的格式与我们在本教程中使用的服饰图像格式相同。

# 我们将使用60000张图像训练网络，并使用10000张图像评估经过学习的网络分类图像的准确率。
# 您可以从tensorflow直接访问fashion mnist，只需导入和加载数据
fashion_mnist = keras.datasets.fashion_mnist
(train_images,train_labels),(test_images,test_labels) = fashion_mnist.load_data()

# 加载数据集会返回4个NumPy数组：
# train_images 和 train_labels数组是训练集，即模型用于学习的数据
# 测试集 test_images 和 test_labels 数组用于测试模型
# 图像为 28 * 28 的Numpy数组，像素值介于0到255之间，标签是整数数组，介于0-9之间。
# 这些标签对应于图像代表的服饰所属的类别：
# 标签	类别
# 0	T 恤衫/上衣
# 1	裤子
# 2	套衫
# 3	裙子
# 4	外套
# 5	凉鞋
# 6	衬衫
# 7	运动鞋
# 8	包包
# 9	踝靴
 
# 每张图像都映射到一个标签。由于数据集中不包含类别名称，因此将它们存储在此处，以便稍后绘制图像时使用：
class_names = ['T-shirt/top','Trouser','Pullover','Dress','Coat',
				'sandal','shirt','sneaker','bag','Ankle boot'] 


# 探索数据
# 我们先探索数据集的格式，然后再训练模型。以下内容显示训练集中有 60000 张图像，每张图像都表示为 28x28 像素：
train_images.shape
>>>(60000,28,28)
# 同样，训练集中有 60000 个标签：
len(train_labels)
>>>60000
# 每个标签都是一个介于0到9之间的整数
train_labels
>>>array([9,0,0,...,3,0,5],dtype=uint8)
# 测试集中有10000张图像。同样，每张图像都表示为 28x28 像素：
test_images.shape
>>>(10000,28,28)
# 测试集中有 10000 个图像标签：
len(test_labels)
>>>10000


# 预处理数据
# 必须对数据进行预处理，然后再训练网络。如果检查训练集中的第一张图像，就会发现像素值介于0到255
plt.figure()
plt.imshow(train_images[0])
plt.colorbar()
plt.grid(False)
# 我们将这些值缩小到0-1之间，然后将其反馈到神经网络模型。为此，将图像组件的数据类型从整数转换为浮点数，然后除以255，以下是预处理图像的函数：
# 务必要以相同的方式对训练集和测试集进行预处理：
train_images = train_images / 255.0
test_images = test_images / 255.0
#显示训练集中的前25张图像，并在每张图像下显示类别名称。验证确保数据格式无误，就可以开始构建 + 训练网络了。
plt.figure(figsize=(10,10))
for i in range(25):
	plt.subplot(5,5,i+1)
	plt.xticks([])
	plt.yticks([])
	plt.grid(False)
	plt.imshow(train_images[i], cmap = plt.cm.binary)
	plt.xlabel(class_names[train_labels[i]])


# 构建模型
# 构建神经网络需要先配置模型的层，然后编译模型

# 设置层
# 神经网络的基本构造块是层。层从馈送到其中的数据提取表示结果。希望这些表示结果有助于解决手头问题。
# 大部分深度学习都会把简单的层连在一起。大部分层（例如tf.keras.layers.Dense）都具有在训练期间要学习的参数
model = keras.Sequential([
	keras.layers.Flatten(input_shape=(28,28)),
	keras.layers.Dense(128, activation=tf.nn.relu),
	keras.layers.Dense(10,activation=tf.nn.softmax)
	])

# 该网络中第一层tf.keras.layers.Flatten将图像格式从二维数组(28 * 28)转换成一维数组。
# 可以将该层视为图像中像素为堆叠的行，并排列这些行。
# 
# 在扁平化像素之后，该网络包含两个tf.keras.layers.Dense层的序列。这些层是密集连接或
# 全连接神经层。第一个Dense层具有128个节点（或神经元）。第二个（也是最后一个）层具有10个节点的softmax层，该层会返回一个具有10个概率得分的数组
# 这些得分的总和为1，每个节点包含一个得分，表示当前图像属于10个类别中某一个的概率。


# 编译模型
# 模型还需要再进行几项设置才可以开始训练。这些设置会添加到模型的编译步骤中：
# 	1.损失函数-衡量模型在训练期间的准确率。我们希望尽可能缩小该函数，以“引导”模型朝着正确的方向优化。
# 	2.优化器-根据模型看到的数据及其损失函数更新模型的方式
# 	3.指标-用于监控训练和测试步骤。以下示例使用准确率，即图像被正确分类的比例。

model.compile(optimizer = tf.train.AdamOptimizer(),
			loss = 'sparse_categorical_crossentropy',
			metrics = ['accuracy'])

# 训练模型
# 训练神经网络模型需要执行以下步骤：
# 1.将训练数据馈送到模型中，在本示例中为train_images和train_labels数组
# 2.模型学习将图像与标签相关联。
# 3.我们要求模型对测试集进行预测，在本示例中为test_images数组。我们会验证预测结果是否与test_labels数组中的标签一致。
# 要开始训练，请调用 model.fit方法，使模型与训练数据“拟合”：
model.fit(train_images,train_labels,epochs=5)

# 评估准确率
# 接下来，比较一下模型在测试数据集上的表现：
test_loss,test_aoc = model.evaluate(test_images,test_labels)
print('Test accuracy:', test_acc)
# 结果表明，模型在测试数据集上的准确率略低于在训练数据集上的准确率。训练准确率和测试准确率之间的差异表示出现过拟合。如果机器学习模型在新数据上的表现不如在训练数据上的表现，就表示出现过拟合。

# 做出预测
# 模型经过训练后，我们可以使用它对一些图像进行预测
predictions = model.predict(test_images)
# 在本示例中，模型已经预测了测试集中每张图像的标签。我们来看看第一个预测：
>>>predictions[0]
>>>array([4.2577299e-06, 7.2840301e-08, 2.3979945e-08, 2.0671453e-06,
       9.1094840e-08, 1.2096325e-01, 1.5182156e-06, 1.9717012e-01,
       1.2066002e-05, 6.8184656e-01], dtype=float32)

# 预测结果是一个具有 10 个数字的数组。这些数字说明模型对于图像对应于 10 种不同服饰中每一个服饰的“置信度”。我们可以看到哪个标签的置信度值最大：
>>>ng.argmax(predictions[0])
>>>9
# 因此，模型非常确信这张图像是踝靴或属于 class_names[9]。我们可以检查测试标签以查看该预测是否正确：
>>>test_labels[0]
>>>9


# 我们可以将该预测绘制成图来查看全部10个通道
def plot_image(i,predictions_array,true_label,img):
	predictions_array,true_label,img = predictions_array[i],true_label[i],img[i]
	plt.grid(False)
	plt.xticks([])
	plt.yticks([])

	plt.imshow(img,cmap = plt.cm.binary)

	predicted_label = np.argmax(predictions_array)
	if predicted_label == true_label:
		color = 'blue'
	else:
		color = 'red'

	plt.xlabel("{} {:2.0f}% ({})".format(class_names[predicted_label],
										100 * np.max(predictions_array),
										class_names[true_label]),
										color = color)

def plot_value_array(i,predictions_array,true_label):
	predictions_array,true_label = predictions_array[i],true_label[i]
	plt.grid(False)
	plt.xticks([])
	plt.yticks([])
	thisplot = plt.bar(range(10),predictions_array,color="#777777")
	plt.ylim([0,1])
	predicted_label = np.argmax(predictions_array)

	thisplot[predicted_label].set_color('red')
	thisplot[true_label].set_color('blue')

# 我们来看看第0张图像、预测和预测数组
i = 0
plt.figure(figsize=(6,3))
plt.subplot(1,2,1)
plot_image(i,predictions,test_labels,test_images)
plt.subplot(1,2,2)
plot_value_array(i,predictions,test_labels)
# 我们用它们的预测绘制几张图像。正确的预测标签为蓝色，错误的预测标签为红色。数字表示
# 预测标签的百分比（总计为100）。请注意，即使置信度非常高，也可能预测错误

# Plot the first X test images,their predicted label, and the true label
# Color correct predictions in blue,incorrect predictions in red.
num_rows = 5
num_cols = 3
num_images = num_rows * num_cols
plt.figure(figsize=(2*2*num_cols,2*num_rows))
for i in range(num_images):
	plt.subplot(num_rows,2*num_cols,2*i+1)
	plot_image(i,predictions,test_labels,test_images)
	plt.subplot(num_rows,2*num_cols,2*i+2)
	plot_value_array(i,predictions,test_labels)

# Grab an image from the test dataset.
img = test_images[0]
print(img.shape)
>>>(28,28)
# tf.keras模型已经过优化，可以一次性对样本批次或样本集进行预测。
# 因此即使我们我们使用单个图像，仍需要将其添加到列表中：
# add the image to a batch where it's the only member.
img = (np.expand_dims(img,0))
print(1,28,28)
# 现在预测这张图像
predictions_single = model.predict(img)
print(predictions_single)

plot_value_array(0,predictions_single,test_labels) 
_ = plt.xticks(range(10),class_names,rotation=45)
# _在交互窗口下表示表达式的最后一个运算结果
np.argmax(predictions_single[0])
>>>9