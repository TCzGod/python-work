import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 读取数据
file_list = ['1.xlsx', '2.xlsx', '3.xlsx', '4.xlsx', '5.xlsx']
data = pd.DataFrame()

for file in file_list:
    data = data.append(pd.read_excel(file))

# 设置字体为Microsoft YaHei以支持中文显示
sns.set(font='Microsoft YaHei')

# 绘制折线图
plt.figure(figsize=(12, 6))
plt.xticks(rotation=45)
plt.xlabel('时间段')
plt.ylabel('平均分')
plt.title('联考成绩平均分变化')

# 按班级计算平均分
statistics = data.groupby(['时间段', '班级']).agg({
    '平均分': 'mean',
}).reset_index()

# 对每个时间段的班级平均分进行排序
sorted_statistics = statistics.groupby('时间段').apply(lambda x: x.sort_values('平均分', ascending=False)).reset_index(drop=True)

# 绘制折线图
sns.lineplot(x='时间段', y='平均分', hue='班级', data=sorted_statistics)

plt.legend(loc='upper right')
plt.show()

# 输出排序结果
# for time_period in sorted_statistics['时间段'].unique():
#     print(f'时间段 {time_period} 班级平均分排序结果：')
#     print(sorted_statistics[sorted_statistics['时间段'] == time_period][['班级', '平均分']])
#     print()
# 创建一个ExcelWriter对象
writer = pd.ExcelWriter('排序结果.xlsx')

# 输出排序结果到Excel文件中
for time_period in sorted_statistics['时间段'].unique():
    period_statistics = sorted_statistics[sorted_statistics['时间段'] == time_period][['班级', '平均分']]
    period_statistics.to_excel(writer, sheet_name=f'时间段{time_period}', index=False)

# 保存Excel文件
writer.save()
