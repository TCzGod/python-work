import re
import pandas as pd
from openpyxl import Workbook

# 读取Excel文件
df = pd.read_excel('gxshi.xlsx')

# 提取系数项和常数项
coefficients = []
constants = []

for i in range(len(df)):
    red_coefficient, red_constant = re.findall(r'[-+]?\d*\.\d+|\d+', df.loc[i, '红函数关系式'])
    yellow_coefficient, yellow_constant = re.findall(r'[-+]?\d*\.\d+|\d+', df.loc[i, '黄函数关系式'])
    blue_coefficient, blue_constant = re.findall(r'[-+]?\d*\.\d+|\d+', df.loc[i, '蓝函数关系式'])

    coefficients.append([float(red_coefficient), float(yellow_coefficient), float(blue_coefficient)])
    constants.append([float(red_constant), float(yellow_constant), float(blue_constant)])

# 创建新的xlsx文件并写入数据
output_file = 'extracted_coefficients.xlsx'
wb = Workbook()
ws = wb.active

# 写入表头
header = ['波长', '红函数系数', '红函数常数', '黄函数系数', '黄函数常数', '蓝函数系数', '蓝函数常数']
ws.append(header)

# 写入数据
for i in range(len(df)):
    wavelength = df.loc[i, '波长']
    red_coefficient, yellow_coefficient, blue_coefficient = coefficients[i]
    red_constant, yellow_constant, blue_constant = constants[i]

    row_data = [wavelength, red_coefficient, red_constant, yellow_coefficient, yellow_constant, blue_coefficient,
                blue_constant]
    ws.append(row_data)

# 保存文件
wb.save(output_file)
