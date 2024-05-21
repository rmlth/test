import cv2
import numpy as np
lower_red = np.array([156, 43, 46])
upper_red = np.array([180, 255, 255])
lower_green = np.array([35, 43, 46])
upper_green = np.array([77, 255, 255])
image = cv2.imread ('2.png')
hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # 分割红色区域
red_mask = cv2.inRange(hsv_img, lower_red, upper_red)
    # 分割绿色区域
green_mask = cv2.inRange(hsv_img, lower_green, upper_green)

    # 使用形态学操作去除噪声并增强目标区域
kernel = np.ones((5,5), np.uint8)
red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, kernel)
green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_CLOSE, kernel)
contours_red, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours_green, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
def detect_points(image):
    
    
    # 定义红色和绿色的颜色范围

    
    # 寻找红色点的轮廓
    for contour in contours_red:
        # 获取红色点的坐标
        M = cv2.moments(contour)
        if M["m00"] != 0:
            red_center_x = int(M["m10"] / M["m00"])
            red_center_y = int(M["m01"] / M["m00"])

    print("红色点坐标:", red_center_x, red_center_y)

    # 寻找绿色点的轮廓
    for contour in contours_green:
        # 获取绿色点的坐标
        M = cv2.moments(contour)
        if M["m00"] != 0:
            green_center_x = int(M["m10"] / M["m00"])
            green_center_y = int(M["m01"] / M["m00"])

    print("绿色点坐标:", green_center_x, green_center_y)
    for contour in contours_red:
            # 获取轮廓的边界框坐标
            x, y, w, h = cv2.boundingRect(contour)
            # 在图像上绘制红色边界框
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)
            # 在图像上标出红色区域的中心坐标
            cv2.putText(image, f'Red: ({x + w // 2}, {y + h // 2})', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    for contour in contours_green:
            # 获取轮廓的边界框坐标
            x, y, w, h = cv2.boundingRect(contour)
            # 在图像上绘制绿色边界框
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            # 在图像上标出绿色区域的中心坐标
            cv2.putText(image, f'Red: ({x + w // 2}, {y + h // 2})', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return image

#def circle_points(image):
    red_points = cv2.findNonZero(red_mask)
    if red_points is not None:
        for point in red_points:
            x, y = point[0]
            cv2.circle(image, (x, y), 5, (255, 0, 0), -1)

    # 找到绿色点
    green_points = cv2.findNonZero(green_mask)
    if green_points is not None:
        for point in green_points:
            x, y = point[0]
            cv2.circle(image, (x, y), 5, (255, 0, 0), -1)

    return image   
# 读取图像



# 调用函数进行检测
result1 = detect_points(image)
cv2.namedWindow('Result1', cv2.WINDOW_NORMAL)
# 显示结果
cv2.imshow('Result1', result1)
#result2 = circle_points(image)
#cv2.namedWindow('Result2', cv2.WINDOW_NORMAL)
# 显示结果
#cv2.imshow('Result2', result2)
cv2.waitKey(0)
cv2.destroyAllWindows()
