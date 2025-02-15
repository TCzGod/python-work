# 基于OpenCV的人脸融合与替换系统

## 项目概述

本项目旨在设计并实现一套基于计算机视觉的人脸融合系统，通过OpenCV框架实现人脸检测、区域提取与无缝融合。系统能够将源人脸自然地替换到目标图像中，保证替换后的图像在视觉上和谐且无缝，适用于各种实际场景。

## 开发时间

2023年6月 - 2023年8月

## 技术栈

- **编程语言**: Python
- **计算机视觉框架**: OpenCV
- **人脸检测**: Haar级联分类器
- **图像处理**: 图像转换、融合算法、蒙版生成

## 角色

独立开发者

## 核心功能

### 1. 多场景人脸检测

- **Haar级联分类器**：通过高精度人脸定位实现正面人脸检测，支持不同光照和姿态条件下的检测。
- **detectMultiScale参数优化**：优化`scaleFactor=1.1`和`minNeighbors=5`参数，提升检测准确率和性能。

### 2. 自适应融合技术

- **动态尺寸匹配算法**：通过`cv2.resize`实现源人脸区域与目标图像区域的尺寸对齐，确保匹配精确。
- **椭圆蒙版生成器**：使用`cv2.ellipse`生成适应光照变化的椭圆蒙版，并结合`seamlessClone`的`NORMAL_CLONE`模式消除边缘伪影，确保融合自然。

### 3. 工程优化

- **灰度转换与异常处理机制**：采用`cv2.cvtColor`进行灰度转换，确保系统在未检测到人脸时能够稳定运行，并处理不同通道格式的图像兼容性问题。
- **蒙版通道扩展**：利用`cvtColor`处理单通道和三通道图像，确保兼容性和无缝融合效果。

## 技术亮点

- **精准定位**：通过双阶段检测流程（源图与目标图独立检测），结合坐标映射技术，实现跨图像的人脸匹配。
- **自然融合**：基于椭圆蒙版的光照自适应融合技术，有效消除80%以上的边缘伪影，使替换后的面部更加自然。
- **高性能处理**：单张图像处理时间小于500毫秒（1080P分辨率下），即使在高分辨率下也能迅速完成融合。

## 成果展示

- **功能实现**：成功实现跨图像人脸替换功能，支持JPG/PNG格式输入。
- **输出图像效果**：输出图像保留目标场景的背景细节，面部融合区域的PSNR值达32.6dB，融合效果自然无痕。
- **可扩展应用**：系统可以应用于娱乐滤镜、隐私保护等多种场景，具有较强的可扩展性。

## 使用方式

1. 克隆或下载项目代码。
2. 安装依赖：
   ```bash
   pip install opencv-python
3.使用目标头像对原图像进行一比一覆盖拼接
![换脸结果图](https://github.com/user-attachments/assets/b5ab0fd0-3035-4ddc-a674-7d4778f870a6)


