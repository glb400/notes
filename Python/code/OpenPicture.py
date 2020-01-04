# 图片的打开与显示

from PIL import Image
img=Image.open('d:/dog.png')
img.show()

# 虽然使用的是Pillow，但它是由PIL fork而来，因此还是要从PIL中进行import. 使用open()函数来打开图片，使用show()函数来显示图片。

# 这种图片显示方式是调用操作系统自带的图片浏览器来打开图片，有些时候这种方式不太方便，因此我们也可以使用另上一种方式，让程序来绘制图片。

from PIL import Image
import matplotlib.pyplot as plt
img=Image.open('d:/dog.png')
plt.figure("dog")
plt.imshow(img)
plt.show()

# figure默认是带axis的，如果没有需要，我们可以关掉

plt.axis('off')

# 打开图片后，可以使用一些属性来查看图片信息，如

print img.size  #图片的尺寸
print img.mode  #图片的模式
print img.format  #图片的格式

# 图片的保存

img.save('d:/dog.jpg')