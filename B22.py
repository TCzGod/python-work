import pandas as pd
import numpy as np
from scipy.optimize import minimize

# 读取数据文件
D65_data = pd.read_excel("D65.xlsx")
tqh_data = pd.read_excel("tqh.xlsx")
attachment3_data = pd.read_excel("附件3.xlsx")

# 提取数据列
wavelength_D65 = D65_data['s']
X_D65 = D65_data['X']
Y_D65 = D65_data['Y']
Z_D65 = D65_data['Z']

wavelength_tqh = tqh_data['s']
X_tqh = tqh_data['X']
Y_tqh = tqh_data['Y']
Z_tqh = tqh_data['Z']

wavelength_attachment3 = attachment3_data['波长']
R1_attachment3 = attachment3_data['R1']

# 计算反射率R
def calculate_R(X_D65, Y_D65, Z_D65, X_tqh, Y_tqh, Z_tqh):
    R = (X_tqh * Y_D65 - X_D65 * Y_tqh) / (Y_D65 * Z_tqh - Z_D65 * Y_tqh)
    return R

# 计算LAB颜色空间中L、a、b值
def calculate_LAB(X_D65, Y_D65, Z_D65, X_tqh, Y_tqh, Z_tqh):
    L = 116 * f(Y_tqh / Y_D65) - 16
    a = 500 * (f(X_tqh / X_D65) - f(Y_tqh / Y_D65))
    b = 200 * (f(Y_tqh / Y_D65) - f(Z_tqh / Z_D65))
    return L, a, b

# 定义目标函数
def objective_function(x):
    R1 = x[0]
    R2 = x[1]
    L1, a1, b1 = calculate_LAB(X_D65, Y_D65, Z_D65, R1*X_tqh, Y_tqh, Z_tqh)
    L2, a2, b2 = calculate_LAB(X_D65, Y_D65, Z_D65, R2*X_tqh, Y_tqh, Z_tqh)
    E = np.sqrt((L1-L2)**2 + (a1-a2)**2 + (b1-b2)**2)
    return E

# 总色差约束
def total_color_difference_constraint(x):
    R1 = x[0]
    R2 = x[1]
    E = objective_function(x)
    return E - 10.0  # 设置总色差阈值为10

# 等式约束
def equality_constraint(x):
    R1 = x[0]
    R2 = x[1]
    return R1_attachment3 - R1, R2_attachment3 - R2

# 初始猜测值
x0 = [0.5, 0.5]  # R1和R2的初始值

# 定义约束条件
constraints = [{'type': 'ineq', 'fun': total_color_difference_constraint},
               {'type': 'eq', 'fun': equality_constraint}]

# 使用最小化方法求解优化问题
result = minimize(objective_function, x0, constraints=constraints)

# 输出结果
print("优化结果：")
print(result)
