import cv2
import numpy as np

lower_red = np.array([0, 0, 100])     # 红色的HSV阈值下限
upper_red = np.array([180, 30, 150])  # 红色的HSV阈值上限

def object_detect(image):
    hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)                       # 图像从BGR颜色模型转换为HSV模型
    mask_red = cv2.inRange(hsv_img, lower_red, upper_red)                  # 图像二值化

    contours, hierarchy = cv2.findContours(mask_red, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE) # 图像中轮廓检测

    for cnt in contours:                                                   # 去除一些轮廓面积太小的噪声
        if cnt.shape[0] < 150:
            continue
            
        (x, y, w, h) = cv2.boundingRect(cnt)                               # 得到苹果所在轮廓的左上角xy像素坐标及轮廓范围的宽和高
        cv2.drawContours(image, [cnt], -1, (0, 255, 0), 2)                 # 将苹果的轮廓勾勒出来
        cv2.circle(image, (int(x+w/2), int(y+h/2)), 5, (0, 255, 0), -1)   

    return image
       
  

       
image = cv2.imread('1.png')
c = object_detect(image)
#建立一个显示图像的窗口
cv2.namedWindow('apple', cv2.WINDOW_NORMAL)

# 在窗口中显示图像
cv2.imshow('apple', c)

# 等待按键，然后关闭窗口
cv2.waitKey(0)
cv2.destroyAllWindows()


