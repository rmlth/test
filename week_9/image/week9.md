# opencv图像处理
#### HSV颜色空间更容易表示一个特定颜色，通过opencv读取的图片为BGR颜色空间，我们利用cv2.cvtColor()可以轻松实现颜色空间的转变。
#### 在函数之前，我们先大致了解一下HSV基本颜色分量范围（通过实验得到的模糊范围，实际操作中我们可以据此做出适当调整）。
![alt text](image.png)