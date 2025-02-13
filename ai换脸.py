import cv2
import numpy as np

# 加载人脸级联分类器
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# 读取图片1
image1 = cv2.imread("joker_face.png")

# 将图片1转换为灰度图
gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)

# 检测图片1中的人脸
faces1 = face_cascade.detectMultiScale(gray_image1, scaleFactor=1.1, minNeighbors=5)

# 读取图片2
image2 = cv2.imread("my2.png")

# 将图片2转换为灰度图
gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

# 检测图片2中的人脸
faces2 = face_cascade.detectMultiScale(gray_image2, scaleFactor=1.1, minNeighbors=5)

# 确保每张图片都有检测到人脸
if len(faces1) > 0 and len(faces2) > 0:
    # 选择第一张图片的第一个人脸
    (x1, y1, w1, h1) = faces1[0]

    # 选择第二张图片的第一个人脸
    (x2, y2, w2, h2) = faces2[0]

    # 从图片1中提取人脸部分
    face_region1 = image1[y1:y1+h1, x1:x1+w1]

    # 调整人脸部分的大小以适应图片2中的人脸尺寸
    resized_face_region1 = cv2.resize(face_region1, (image2.shape[1], image2.shape[0]))

    # 创建与image2相同大小的蒙版
    mask = np.zeros((image2.shape[0], image2.shape[1]), dtype=np.uint8)

    # 绘制蒙版中的椭圆区域，在人脸边界处添加渐变效果
    center = ((x2 + x2 + w2) // 2, (y2 + y2 + h2) // 2)
    axes = (w2 // 2, h2 // 2)
    cv2.ellipse(mask, center, axes, 0, 0, 360, (255, 255, 255), -1)

    # 进行无缝融合
    blended_image = cv2.seamlessClone(resized_face_region1, image2, mask, center, cv2.NORMAL_CLONE)

    # 显示结果图片
    cv2.imshow("Face Swap", blended_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("未检测到人脸")
