import cv2
import numpy as np

# 定义红色和绿色的颜色范围
lower_red = np.array([0, 100, 100])
upper_red = np.array([10, 255, 255])
lower_green = np.array([40, 100, 100])
upper_green = np.array([80, 255, 255])
lower_black = np.array([0, 0, 0])     # 红色的HSV阈值下限
upper_black = np.array([180, 35, 160])  # 红色的HSV阈值上限
def detect_lines_and_points(image):
    image_copy = image.copy()
    hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)                       # 图像从BGR颜色模型转换为HSV模型
    mask_black = cv2.inRange(hsv_img, lower_black, upper_black)                  # 图像二值化

    contours, hierarchy = cv2.findContours(mask_black, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE) # 图像中轮廓检测
    for cnt in contours:
        if cnt.shape[0] < 150:
            continue
            
        (x, y, w, h) = cv2.boundingRect(cnt)                               # 得到苹果所在轮廓的左上角xy像素坐标及轮廓范围的宽和高
        cv2.drawContours(image, [cnt], -1, (0, 255, 0), 2)                 # 将苹果的轮廓勾勒出来
        cv2.circle(image, (int(x+w/2), int(y+h/2)), 5, (0, 255, 0), -1)   

    
    # 在图像中寻找红点
    red_mask = cv2.inRange(image_copy, lower_red, upper_red)
    red_points = cv2.findNonZero(red_mask)
    if red_points is not None:
        for point in red_points:
            x, y = point[0]
            print("红点坐标：", (x, y))
            cv2.circle(image, (x, y), 5, (0, 0, 255), -1)

    # 在图像中寻找绿点
    green_mask = cv2.inRange(image_copy, lower_green, upper_green)
    green_points = cv2.findNonZero(green_mask)
    if green_points is not None:
        for point in green_points:
            x, y = point[0]
            print("绿点坐标：", (x, y))
            cv2.circle(image, (x, y), 5, (0, 255, 0), -1)

    return image_copy

# 读取图像
image = cv2.imread('1.png')
# 调用函数进行检测
result = detect_lines_and_points(image)
# 显示结果
#创建可调整大小的窗口
cv2.namedWindow('Result', cv2.WINDOW_NORMAL)
cv2.imshow('Result', result)
cv2.waitKey(0)
cv2.destroyAllWindows()
