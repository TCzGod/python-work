import numpy as np
import pandas as pd
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

# 读取 Excel 文件
idx = 2
df = pd.read_excel(r'./附件%d.xlsx' % idx, engine='openpyxl', skiprows=1)

# 处理合并单元格
for idx, row in df.iterrows():
    if pd.isna(row[0]):
        df.loc[idx, 'Unnamed: 0'] = df.loc[idx-1, 'Unnamed: 0']

# 设置第一列和第二列为索引
df = df.set_index(['Unnamed: 0', '浓度（%）'])

# 定义 x 轴数据
x = [0.05, 0.1, 0.5, 1, 2, 3, 4, 5]

# 对红色数据进行拟合和评价
for i in range(len(df.columns)):
    y = np.array(df.loc['红'].iloc[:, i])
    # 计算回归系数
    slope, intercept = np.polyfit(x, y, 1)
    # 函数关系式
    print('K/S = %f * x + %f' % (slope, intercept))
    # 拟合结果
    y_pred = slope * np.array(x) + intercept
    # 计算决定系数（R^2）
    r2 = r2_score(y, y_pred)
    print("R^2:", r2)
    # 计算均方误差（MSE）
    mse = mean_squared_error(y, y_pred)
    print("MSE:", mse)
    # 计算均方根误差（RMSE）
    rmse = np.sqrt(mse)
    print("RMSE:", rmse)
    # 计算平均绝对误差（MAE）
    mae = mean_absolute_error(y, y_pred)
    print("MAE:", mae)

# 对蓝色数据进行拟合和评价
for i in range(len(df.columns)):
    y = np.array(df.loc['蓝'].iloc[:, i])
    # 计算回归系数
    slope, intercept = np.polyfit(x, y, 1)
    # 函数关系式
    print('K/S = %f * x + %f' % (slope, intercept))
    # 拟合结果
    y_pred = slope * np.array(x) + intercept
    # 计算决定系数（R^2）
    r2 = r2_score(y, y_pred)
    print("R^2:", r2)
    # 计算均方误差（MSE）
    mse = mean_squared_error(y, y_pred)
    print("MSE:", mse)
    # 计算均方根误差（RMSE）
    rmse = np.sqrt(mse)
    print("RMSE:", rmse)
    # 计算平均绝对误差（MAE）
    mae = mean_absolute_error(y, y_pred)
    print("MAE:", mae)
