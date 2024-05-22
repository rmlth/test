import cv2
import numpy as np

def detect_target_rectangle(image_path):#检测目标矩形
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)#转换为灰度图
    blur = cv2.GaussianBlur(gray, (5, 5), 0)#高斯模糊
    edges = cv2.Canny(blur, 50, 150, apertureSize=3)#边缘检测
    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)#寻找轮廓

    target_rectangle = None # 目标矩形
    min_distance = float('inf')#最小距离
    image_center = (image.shape[1] // 2, image.shape[0] // 2)#图像中心
    for contour in contours:#遍历轮廓
        perimeter = cv2.arcLength(contour, True)#周长
        approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)#逼近
        if len(approx) == 4 and cv2.contourArea(approx) > 50:#判断是否是矩形
            M = cv2.moments(approx)#计算矩形中心
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            distance = np.sqrt((cx - image_center[0]) ** 2 + (cy - image_center[1]) ** 2)#计算距离
            if distance < min_distance:#   判断是否是最近的矩形
                min_distance = distance# 更新最小距离和矩形
                print(distance)
                target_rectangle = approx# 更新目标矩形

    if target_rectangle is not None: # 如果找到了目标矩形
        cv2.drawContours(image, [target_rectangle], -1, (0, 255, 0), 2)#绘制目标矩形
        M = cv2.moments(target_rectangle)#计算矩形中心
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        cv2.circle(image, (cx, cy), 5, (0, 0, 255), -1)
        cv2.putText(image, f'({cx}, {cy})', (cx + 10, cy + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)#绘制矩形中心
        print(1)
        for point in target_rectangle:#绘制矩形四个点
            x, y = point[0]
            cv2.circle(image, (x, y), 5, (255, 0, 0), -1)
            cv2.putText(image, f'({x}, {y})', (x + 10, y + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    return image

image_path = 'week_9/code/src/2.png'
result_image = detect_target_rectangle(image_path)
cv2.namedWindow('Result1', cv2.WINDOW_NORMAL)
cv2.imshow('Result1', result_image)
cv2.waitKey(0)
cv2.destroyAllWindows()