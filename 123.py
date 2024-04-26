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
        cv2.drawContours(image, [cnt], -1, (0, 255, 0), 2)                 # 将苹果的轮廓勾勒出来
        cv2.circle(image, (int(x+w/2), int(y+h/2)), 5, (0, 255, 0), -1)   

    return image

# 读取一张图片

#img = cv2.imread('1.jpg')
#c = cv2.VideoCapture('http://192.168.1.251:4747/video') 
#c = cv2.VideoCapture(3) 







#while True:
    ret, frame = c.read()

    frame = object_detect(frame)

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('0'): # 按0键退出
        break

#创建可调式窗口
# 读取图像
image = cv2.imread('1ad24cd0e4d41553974bfdd851cb4ed.png')
c = object_detect(image)
# 创建一个窗口并命名为 "Example Window"
cv2.namedWindow('apple', cv2.WINDOW_NORMAL)

# 在窗口中显示图像
cv2.imshow('apple', c)

# 等待按键，然后关闭窗口
cv2.waitKey(0)
cv2.destroyAllWindows()

