import cv2
import numpy as np

from typing import List

def calculate_intersection(vertices):
    """
    计算四边形对角线的交点。

    参数:
    vertices: 一个包含四个顶点坐标的列表, 每个顶点是一个二元组(x, y)。

    返回值:
    如果存在交点, 返回交点的坐标(x, y)；如果不存在交点, 返回None。
    """
    x1, y1 = vertices[0]
    x2, y2 = vertices[2]
    x3, y3 = vertices[1]
    x4, y4 = vertices[3]

    dx1, dy1 = x2 - x1, y2 - y1
    dx2, dy2 = x4 - x3, y4 - y3

    det = dx1 * dy2 - dx2 * dy1

    if det == 0 or (dx1 == 0 and dx2 == 0) or (dy1 == 0 and dy2 == 0):
        return None

    dx3, dy3 = x1 - x3, y1 - y3
    det1 = dx1 * dy3 - dx3 * dy1
    det2 = dx2 * dy3 - dx3 * dy2

    if det1 == 0 or det2 == 0:
        return None

    s = det1 / det
    t = det2 / det

    if 0 <= s <= 1 and 0 <= t <= 1:
        intersection_x = x1 + dx1 * t
        intersection_y = y1 + dy1 * t
        return int(intersection_x), int(intersection_y)
    else:
        return None


def shrink_rectangle(vertices, center_x, center_y, multiple):
    """
    已知四边形四个顶点坐标和中心点坐标, 计算缩小 multiple 倍后的四边形坐标
    """
    small_vertices = []

    for vertex in vertices:
        new_x = int(center_x + (vertex[0] - center_x) * multiple)
        new_y = int(center_y + (vertex[1] - center_y) * multiple)
        small_vertices.append([new_x, new_y])

    return np.array(small_vertices, dtype=np.int32)


def average_points(point1, point2, N):
    """
    根据两个给定点和分段数N, 计算这两个点之间等分的坐标点列表。
    """
    delta_x = (point2[0] - point1[0]) / N
    delta_y = (point2[1] - point1[1]) / N
    
    points_list = []
    
    for i in range(N+1):
        x = point1[0] + delta_x * i
        y = point1[1] + delta_y * i
        points_list.append([x, y])
    
    return points_list

def draw_line_points(image, small_vertices, line_seg_num):
    """
    绘制等分点
    """
    for i, j in [0, 1], [1, 2], [2, 3], [3, 0]:
        points_list = average_points(small_vertices[i], small_vertices[j], line_seg_num)
        for point in points_list:
            x, y = point
            cv2.circle(image, (int(x), int(y)), 4, (0, 0, 255), -1)
            #print(int(x),int(y))
        #print("----------")
    return image

def pre_cut(image):
    # 指定裁剪区域的坐标和尺寸
    """ x = 175  # 左上角x坐标
    y = 0  # 左上角y坐标
    w = 940  # 宽度
    h = 660  # 高度 """

    
    x = 162  # 左上角x坐标
    y = 20  # 左上角y坐标
    w = 854  # 宽度
    h = 480  # 高度

    return image[y:y+h, x:x+w]
def preprocess_image(img):

    """
    对输入图像进行预处理, 包括灰度转换、高斯模糊、Canny边缘检测, 并返回其中的轮廓信息。
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 转换为灰度图像

    blur = cv2.GaussianBlur(gray, (1, 1), 0)  # 高斯滤波去噪

    # 减小曝光
    #exposure_adjusted = cv2.addWeighted(blur, 0.5, np.zeros(blur.shape, dtype=blur.dtype), 0, 50)

    # 增加对比度（直方图均衡化）
    #blur = cv2.convertScaleAbs(blur, alpha=0.5, beta=-50)
    #blur = cv2.convertScaleAbs(blur, alpha=1, beta=-120)

    #_, blur = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    #_, threshold = cv2.threshold(blur, 157, 255, cv2.THRESH_BINARY) # 二值化
    #edges = cv2.Canny(threshold, 10, 200)  # 使用Canny算子进行边缘检测
    edges = cv2.Canny(blur, 50, 200)

    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # 查找轮廓
    return contours


def find_max_perimeter_contour(contours, max_allowed_perimeter, min_allowed_perimeter):
    # 输入参数校验
    if not contours or max_allowed_perimeter <= 0:
        raise ValueError("输入的轮廓列表不能为空, 且最大允许周长必须为正数。")

    # 初始化最大周长及对应轮廓变量, 以及标志位表示是否找到符合条件的轮廓
    max_perimeter = 0
    vertices = None

    # 遍历轮廓列表
    for cnt in contours:
        # 将当前轮廓近似为四边形
        approx = cv2.approxPolyDP(cnt, 0.09 * cv2.arcLength(cnt, True), True)

        # 确保转换后的形状为四边形
        if len(approx) == 4:
            # 计算四边形周长
            perimeter = cv2.arcLength(approx, True)
            perimeter_allowed = (perimeter <= max_allowed_perimeter) and (perimeter >= min_allowed_perimeter)
            
            if perimeter_allowed and perimeter > max_perimeter:
                # 计算四边形角度
                cosines = []
                for i in range(4):
                    p0 = approx[i][0]
                    p1 = approx[(i + 1) % 4][0]
                    p2 = approx[(i + 2) % 4][0]
                    v1 = p0 - p1
                    v2 = p2 - p1
                    cosine_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
                    angle = np.arccos(cosine_angle) * 180 / np.pi
                    cosines.append(angle)

                # 若当前轮廓周长在允许范围内、大于当前最大周长且角度大于等于N度
                if all(angle >= 30 for angle in cosines):
                    max_perimeter = perimeter
                    vertices = approx.reshape(4, 2)

    # 检查是否找到符合条件的轮廓
    if vertices is None:
        # 返回空列表代替None, 或可选择抛出异常
        return None
    else:
        return vertices

def roi_cut(image, vertices):
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, [vertices], (255, 255, 255))
    masked_image = cv2.bitwise_and(image, mask)

    return masked_image

def find_point(image):

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    def find_max_contours(mask):
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) > 0:
            # 找到最大的轮廓
            largest_contour = max(contours, key=cv2.contourArea)
            # 找到最大轮廓的外接矩形
            x, y, w, h = cv2.boundingRect(largest_contour)  
            
            center_x = x + w / 2  # 计算中心点 x 坐标
            center_y = y + h / 2  # 计算中心点 y 坐标

            point = [x, y, w, h, center_x, center_y]
            # print(point)
            return point
        else:
            return [0,0,0,0,0,0]
        
    def find_red_point(hsv):
        lower = np.array([0, 100, 100])
        upper = np.array([10, 255, 255])
        mask1 = cv2.inRange(hsv, lower, upper)

        lower = np.array([160, 100, 100])
        upper = np.array([179, 255, 255])
        mask2 = cv2.inRange(hsv, lower, upper)

        mask = mask1 | mask2

        return find_max_contours(mask)
    def find_green_point(hsv):
        # 绿色范围
        lower = np.array([40, 100, 100])
        upper = np.array([80, 255, 255])
        mask = cv2.inRange(hsv, lower, upper)

        return find_max_contours(mask)
    
    def find_yellow_point(hsv):
        lower = np.array([26, 43, 46])
        upper = np.array([34, 255, 255])
        mask = cv2.inRange(hsv, lower, upper)
        return find_max_contours(mask)
    
    def find_white_point(hsv):
        lower = np.array([0, 0, 200])
        upper = np.array([180, 30, 255])
        mask = cv2.inRange(hsv, lower, upper)
        return find_max_contours(mask)

    red_point = find_red_point(hsv)
    green_point = find_green_point(hsv)

    if red_point[0] == 0 or green_point[0] == 0:
        yellow_point = find_yellow_point(hsv)
        red_point    = yellow_point
        green_point  = yellow_point
        print("\n红绿光重叠, 找黄光\n")

        if yellow_point[0] == 0:
            white_point = find_white_point(hsv)
            red_point   = white_point
            green_point = white_point
            print("\n黄光找不到, 找白光\n")

    return red_point, green_point

def draw_point(image, point, bgr = ( 0, 255, 255) , color = ' '):

    [x, y, w, h, center_x, center_y] = point
    # 在图像上绘制方框
    cv2.rectangle(image, (x, y), (x + w, y + h), bgr, 1)

    # 绘制坐标
    text = f"{color} point: ({center_x}, {center_y})"
    cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, bgr, 1)

    return image


def draw_contour_and_vertices(img: cv2.Mat, vertices: List[List[int]], scale: float) -> cv2.Mat:
    """
    在图像上绘制四边形的轮廓、顶点、对角线、交点, 并等比缩小重新绘制。
    
    :param img: 输入的OpenCV图像
    :param vertices: 四边形的顶点列表, 格式为[[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
    :param scale: 缩小比例
    :return: 绘制后的图像
    """
    small_vertices = []
    
    try:   
        if vertices is not None:
            # 将四边形顶点列表转换为适合drawContours()的格式
            contour = np.array([vertices], dtype=np.int32)  
            cv2.drawContours(img, [contour], 0, (255, 0, 0), 2)  
        else: 
            print("顶点无效或缺失,跳过轮廓绘制。")  

        for i, vertex in enumerate(vertices):  # 绘制每个角点和坐标
            cv2.circle(img, (vertex[0], vertex[1]), 5, (0, 0, 255), -1)
            cv2.putText(
                img,
                f"({vertex[0]}, {vertex[1]})",
                (vertex[0] + 5, vertex[1] - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (0, 0, 255), 1, cv2.LINE_AA,
            )

        cv2.line(  # 绘制对角线
            img,
            (vertices[0][0], vertices[0][1]),
            (vertices[2][0], vertices[2][1]),
            (0, 255, 0), 1,
        )
        cv2.line(
            img,
            (vertices[1][0], vertices[1][1]),
            (vertices[3][0], vertices[3][1]),
            (0, 255, 0), 1,
        )
        
        intersection = calculate_intersection(vertices)  # 计算两个对角线的交点

        # 绘制交点和坐标
        if intersection is not None:
            cv2.circle(
                img, (int(intersection[0]), int(intersection[1])), 5, (0, 0, 255), -1
            )
            cv2.putText(
                img,
                f"({int(intersection[0])}, {int(intersection[1])})",
                (int(intersection[0]) + 5, int(intersection[1]) - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (0, 0, 255), 1, cv2.LINE_AA,
            )
        
            # 绘制等比缩小后的图像
            """ small_vertices = shrink_rectangle(
                vertices, intersection[0], intersection[1], scale
            ) """

            _, inv_M = persp_trans(img, vertices)  # 获取透视变换矩阵
            
            small_vertices = shrink_rectangle_new(img, scale)  # 缩小矩形

            small_vertices = inv_trans_vertices(small_vertices, inv_M)


            cv2.drawContours(img, [small_vertices], 0, (255, 0, 0), 2)  # 绘制四边形的边框

            for vertex in small_vertices:
                cv2.circle(img, vertex, 5, (0, 0, 255), -1)
                cv2.putText(
                    img,
                    f"({int(vertex[0])}, {int(vertex[1])})",
                    (vertex[0] + 5, vertex[1] - 5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 0, 255), 1, cv2.LINE_AA,
                )

    except Exception as e:
        print(f"绘制过程中发生错误: {e}")
    
    return img, small_vertices

####################################################

def persp_trans(img, vertices):
    # 对四边形顶点坐标进行排序
    rect = np.zeros((4, 2), dtype="float32")
    rect[0] = vertices[0]
    rect[1] = vertices[3]
    rect[2] = vertices[2]
    rect[3] = vertices[1]

    height, width = img.shape[:2]  # 获取图像的高度和宽度

    # 定义目标矩形的顶点坐标，即变换后的图像矩形框
    dst = np.array([[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]], dtype="float32")

    # 计算透视变换矩阵
    M = cv2.getPerspectiveTransform(rect, dst)
    inv_M = np.linalg.inv(M)

    # 返回变换后的图像及变换矩阵
    return M, inv_M

def draw_warped_image(img, M, inv_M):    # 用于检查变换效果

    height, width = img.shape[:2]  # 获取图像的高度和宽度

    # 应用透视变换到图像上
    warped_image = cv2.warpPerspective(img, M, (width, height))

    # 应用逆透视变换到图像
    inv_warped_image = cv2.warpPerspective(warped_image, inv_M,  (width, height))
    
    return warped_image, inv_warped_image


def shrink_rectangle_new(img, scale):
    """
    参数:
    img: 一个数组，代表图像
    scale: 缩小的比例因子，表示新矩形的大小是原矩形大小的scale倍。

    返回值:
    返回一个类型为numpy.int32的二维数组，包含四个点的坐标，这四个点分别代表缩小后矩形的四个顶点。
    """

    height, width = img.shape[:2]

    rectangle_vertices = [[],[],[],[]]
    
    rectangle_vertices[0] = [0, 0]
    rectangle_vertices[1] = [0, height]
    rectangle_vertices[2] = [width, height]
    rectangle_vertices[3] = [width, 0]

    #print (rectangle_vertices)

    center_x = width // 2
    center_y = height // 2

    small_vertices = []

    for vertex in rectangle_vertices:
        new_x = int(center_x + (vertex[0] - center_x) * scale)
        new_y = int(center_y + (vertex[1] - center_y) * scale)
        small_vertices.append([new_x, new_y])

    #print (small_vertices)

    return np.array(small_vertices, dtype=np.int32)


def inv_trans_vertices(small_vertices, inv_M):
    """
    反变换顶点集合
    
    参数:
    small_vertices: 一个二维数组，代表待变换的顶点集合，每个顶点为2D坐标。
    inv_M: 一个4x4的矩阵，代表待应用的逆变换矩阵。
    
    返回值:
    一个二维数组，表示应用逆变换后的顶点集合，顶点仍为2D坐标，但取整至最接近的整数。
    """
    
    vertices_array = np.array(small_vertices, dtype=np.float32)
    vertices_homo = np.concatenate([vertices_array, np.ones((vertices_array.shape[0], 1))], axis=1)
    
    inv_trans_vertices_homo = np.dot(inv_M, vertices_homo.T).T
    inv_trans_vertices = inv_trans_vertices_homo[:, :2] / inv_trans_vertices_homo[:, 2, None]
    
    inv_trans_vertices_int = inv_trans_vertices.astype(int)

    return inv_trans_vertices_int

#################################################################

img = None

if __name__ == "__main__":
    print("开始")
    
    # 读取图像
    img = cv2.imread('2.png')
    
    # 预处理图像，获取轮廓
    contours = preprocess_image(img)

    # 如果轮廓不为空，则寻找具有最大周长的矩形
    if contours is not None:
        vertices = find_max_perimeter_contour(contours, 10090*4, 200*4)
        
    # 如果找到了轮廓的顶点，则进行ROI切割，并寻找红点和绿点
    if vertices is not None:
        
        # 根据顶点进行ROI区域切割
        roi_img = roi_cut(img, vertices)
        
        # 在ROI图像中寻找红点和绿点
        red_point, green_point = find_point(roi_img)
        
        # 如果找到红点，则在原图上标注红点
        if red_point is not None:
            draw_point(img, red_point, color = 'red ')
        
        # 如果找到绿点，则在原图上标注绿点
        if green_point is not None:
            draw_point(img, green_point, color = 'green ')

        # 在原图上绘制轮廓和顶点
        img, _ = draw_contour_and_vertices(img, vertices, (5/6))  # 绘制轮廓和顶点，调整比例因子

    # 显示处理后的图像，并保存
    cv2.imshow("final", img)
    cv2.imwrite("week_9/code/out/2.1out.png", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()