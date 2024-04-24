# 在工作中获得的方法
* 代码发现运行不如预期，把核心部分代码单独拿出来，通过改一些数据，运用控制变量法，找到问题所在。
### 举例
```  bash
import cv2
import numpy as np

lower_red = np.array([0, 90, 128])     # 红色的HSV阈值下限
upper_red = np.array([180, 255, 255])  # 红色的HSV阈值上限

def object_detect(image):
    hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)                       # 图像从BGR颜色模型转换为HSV模型
    mask_red = cv2.inRange(hsv_img, lower_red, upper_red)                  # 图像二值化

    contours, hierarchy = cv2.findContours(mask_red, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE) # 图像中轮廓检测

    for cnt in contours:                                                   # 去除一些轮廓面积太小的噪声
        if cnt.shape[0] < 150:
            continue
            
        (x, y, w, h) = cv2.boundingRect(cnt)                               # 得到苹果所在轮廓的左上角xy像素坐标及轮廓范围的宽和高

        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.drawContours(image, [cnt], -1, (0, 255, 0), 2)                 # 将苹果的轮廓勾勒出来
        cv2.circle(image, (int(x+w/2), int(y+h/2)), 5, (0, 255, 0), -1)

    return image

# 读取一张图片

#img = cv2.imread('1.jpg')
c = cv2.VideoCapture('http://192.168.1.251:4747/video?320x240') 
#c = cv2.VideoCapture(2) 
while True:
    ret, frame = c.read()
    
    frame = object_detect(frame)
    

    #创建可调试窗口
    cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 显示图片
#cv2.imshow('image', img)
```
* 通过c = cv2.VideoCapture('http://192.168.1.251:4747/video?320x240') ，改变里面的地址，就可以实现摄像头的实时监控。
0,1,2看看分别对应摄像头的编号。
* 发现很卡，就控制地址，改变分辨率，然后就看是不是算法不好，在注释算法看还不卡，就改算法。