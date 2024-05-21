import cv2
import numpy as np

# 读取图像
image_path = 'D:/git/test/week_9/code/src.png'
image = cv2.imread(image_path)

if image is None:
    raise ValueError(f"无法从 {image_path} 加载图像")

# 转换为 HSV 颜色空间
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# 定义黑色的 HSV 颜色范围
lower_black = np.array([0, 0, 0])
upper_black = np.array([180, 255, 50])

# 创建掩膜
mask = cv2.inRange(hsv_image, lower_black, upper_black)

# 使用掩膜提取黑色区域
res = cv2.bitwise_and(image, image, mask=mask)

# 找到轮廓
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 遍历轮廓，找到目标矩形
for contour in contours:
    # 获取最小外接矩形
    rect = cv2.minAreaRect(contour)
    box = cv2.boxPoints(rect)
    box = np.int0(box)

    # 计算矩形面积
    width = rect[1][0]
    height = rect[1][1]
    area = width * height

    # 根据面积和宽高比筛选出细黑线矩形
    if area > 1000 and min(width, height) / max(width, height) < 0.1:
        # 绘制矩形
        cv2.drawContours(image, [box], 0, (0, 255, 0), 2)

# 显示结果
cv2.imshow('Detected Rectangle', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
