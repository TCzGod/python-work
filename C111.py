import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 读取聚类结果文件
data = pd.read_csv('data_K.csv')

# 根据聚类结果进行用户画像
user_profiles = []

for cluster_id in range(data['kmeans'].nunique()):
    cluster_data = data[data['kmeans'] == cluster_id]

    # 提取该聚类的用户特征
    user_profile = {
        'Cluster ID': cluster_id,
        'App Class': cluster_data['app_class'].sum(),
        'App Type': cluster_data['app_type'].sum(),
        'App Count': cluster_data['app_count'].sum(),
        'Start Time Avg': cluster_data['start_time_avg'].sum(),
        'End Time Avg': cluster_data['end_time_avg'].sum(),
        'Duration Sum': cluster_data['duration_sum'].sum(),
        'Duration Avg': cluster_data['duration_avg'].sum(),
        'Up Flow Sum': cluster_data['up_flow_sum'].sum(),
        'Down Flow Sum': cluster_data['down_flow_sum'].sum(),
        'Up Flow Avg': cluster_data['up_flow_avg'].sum(),
        'Down Flow Avg': cluster_data['down_flow_avg'].sum()
    }
    user_profiles.append(user_profile)

# 提取用户群体 ID 和用户数量
cluster_ids = [profile['Cluster ID'] for profile in user_profiles]
feature_names = ['App Class', 'App Type', 'App Count', 'Start Time Avg','End Time Avg', 'Duration Sum', 'Duration Avg',
                 'Up Flow Sum','Down Flow Sum', 'Up Flow Avg', 'Down Flow Avg']
feature_values = [[profile[feature] for feature in feature_names] for profile in user_profiles]

# 转换为 NumPy 数组
feature_values = np.array(feature_values)

# 创建热力图
fig, ax = plt.subplots(figsize=(10, 8))
heatmap = ax.imshow(feature_values, cmap='coolwarm', vmin=feature_values.min(), vmax=feature_values.max())

# 添加颜色条
cbar = plt.colorbar(heatmap)

# 设置坐标轴标签和标题
ax.set_xticks(range(len(feature_names)))
ax.set_yticks(range(len(cluster_ids)))
ax.set_xticklabels(feature_names, rotation=45)
ax.set_yticklabels(cluster_ids)
ax.set_xlabel('Feature')
ax.set_ylabel('Cluster ID')
ax.set_title('Cluster Feature Heatmap')

# 显示图形
plt.show()
