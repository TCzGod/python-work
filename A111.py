import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 读取数据
file_list = ['1.xlsx']
data = pd.DataFrame()

for file in file_list:
    data = data.append(pd.read_excel(file))

# 统计每位班主任的最高分、最低分、平均分、优秀率、良好率、合格率、低分率、超均率和标准差
statistics = data.groupby('班级').agg({
    '平均分': 'mean',
}).reset_index()

# 设置字体为Microsoft YaHei以支持中文显示
sns.set(font='Microsoft YaHei')

# 绘制折线图
plt.figure(figsize=(12, 6))
plt.xticks(rotation=45)
plt.xlabel('指标')
plt.ylabel('得分')
plt.title('班主任成绩统计')

# 绘制折线图
for col in statistics.columns[1:]:
    sns.lineplot(x='班级', y=col, data=statistics, label=col)

plt.legend(loc='upper right')
plt.show()
