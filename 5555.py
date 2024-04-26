import cv2
import numpy as np

def detect_points(image):
    hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # 定义红色和绿色的颜色范围
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])
    lower_green = np.array([40, 100, 100])
    upper_green = np.array([80, 255, 255])

    # 分割红色区域
    red_mask = cv2.inRange(hsv_img, lower_red, upper_red)
    # 分割绿色区域
    green_mask = cv2.inRange(hsv_img, lower_green, upper_green)

    # 使用形态学操作去除噪声并增强目标区域
    kernel = np.ones((5,5), np.uint8)
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, kernel)
    green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_CLOSE, kernel)

    # 找到红色点
    red_points = cv2.findNonZero(red_mask)
    if red_points is not None:
        for point in red_points:
            x, y = point[0]
            cv2.circle(image, (x, y), 5, (0, 0, 255), -1)

    # 找到绿色点
    green_points = cv2.findNonZero(green_mask)
    if green_points is not None:
        for point in green_points:
            x, y = point[0]
            cv2.circle(image, (x, y), 5, (0, 255, 0), -1)

    return image

# 读取图像
image = cv2.imread('1.png')
# 调用函数进行检测
result = detect_points(image)
# 显示结果
cv2.imshow('Result', result)
cv2.waitKey(0)
cv2.destroyAllWindows()
