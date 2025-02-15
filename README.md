# 基于多模态机器学习的移动用户行为分析与预测系统

系统主要解决以下问题：

1. 结合多种模型方法，选择合理的聚类数量，根据用户常用所属的20类APP的数据进行聚类，并对结果进行比较分析；
2. 根据问题1得到的分析结果，对不同的用户进行用户画像处理，并描述不同用户的属性特征；
3. 根据用户第1到11天的A类APP的使用情况，来预测用户在第12~21天是否会使用该类APP，并给出预测结果的准确率；
4. 根据用户第1到11天的A类APP的使用情况，来预测用户在第12~21天使用A类APP的有效日均使用时长，并计算评价指标NMSE。

## 系统设计流程图
![系统设计流程图](https://github.com/user-attachments/assets/78938a4b-8c4f-4925-b330-549d6d5e345a)

## 前期数据分析与处理

### 数据分析

#### 相关性矩阵

通过计算Pearson和Spearman相关性矩阵，了解各特征之间的关系。

![相关性矩阵](https://github.com/user-attachments/assets/30faa57b-96c5-4da5-bf83-74afb85074d3)

#### 特征变量散点分布图

通过绘制散点图，展示特征变量之间的关系。

![特征变量散点分布图](https://github.com/user-attachments/assets/527d3ddd-8652-40d2-bce5-848258f0d57c)

### 数据处理

1. **时间转换**：对start_time与end_time特征转换为一天当中的秒数，便于计算。
2. **去量纲化**：对上行和下行流量进行去量纲化，计算每条样本每秒的上行流量与下行流量。
3. **数据合并与连接**：将用户第1到21天的数据合并，并与app类别数据进行左连接，作为特征数据。
4. **数据编码**：采用LabelEncoder对`uid`、`appid`、`app_class`进行编码，以防止One-Hot编码带来的高维问题。
5. **数据聚合**：通过`uid`和`appid`进行聚合，统计每个用户使用每个app的相关数据。

### 用户画像

根据聚类结果，用户被分为不同类别，以下是几类用户的画像：

![用户画像](https://github.com/user-attachments/assets/dd3b5bae-58eb-41ce-bda5-36456a0599d1)

#### 类别一用户：
- 数据基数：21,842,239
- 平均使用频次前三类别：F, P, T
- 平均上行流量前三类：F, C, G
- 平均下行流量前三类：C, O, F

#### 类别二用户：
- 数据基数：35,806
- 平均使用频次前三类别：G, O, C
- 平均上行流量前三类：O, G, C
- 平均下行流量前三类：C, G, T

#### 类别三用户：
- 数据基数：239,398
- 平均使用频次前三类别：F, H, P
- 平均上行流量前三类：H, Q, G
- 平均下行流量前三类：E, O, C

#### 类别四用户：
- 数据基数：3,387,719
- 平均使用频次前三类别：F, P, A
- 平均上行流量前三类：S, T, C
- 平均下行流量前三类：O, C, T

#### 用户行为综述：
- 用户在下午2-3点使用app频次最高。
- 系统自带app使用频次较少，用户安装的app使用频次占大多数。

---

## ARIMA模型对用户行为预测

### ARIMA模型基本步骤
1. 输入与用户使用A类软件相关的数据；
2. 数据预处理：包括数据清洗、缺失值处理、异常值处理等；
3. 将数据按照时间顺序排列，形成时间序列数据；
4. 选择合适的ARIMA模型参数，观察自相关图（ACF）和偏自相关图（PACF）；
5. 使用ARIMA模型进行训练和验证；
6. 使用训练好的模型进行预测；
7. 输出结果。

#### ARIMA拟合结果：
![ARIMA拟合结果](https://github.com/user-attachments/assets/be508999-59f7-432b-9e9d-675e0c94535e)

---

## 随机森林对用户使用时长的预测

### 随机森林基本步骤
1. 输入与用户使用A类软件相关的数据；
2. 数据预处理：包括数据清洗、缺失值处理、异常值处理等；
3. 划分训练集与测试集；
4. 使用训练集构建随机森林模型；
5. 训练模型，调整参数以优化预测结果；
6. 使用测试集进行模型评估；
7. 输出预测结果。

#### 随机森林拟合结果：
![随机森林拟合结果](https://github.com/user-attachments/assets/75a1a8df-4b6f-4666-b786-8f8b0a9f4cd5)

#### 其中涉及到的sql代码
```--------聚类----------
 if object_id('data_1') is not null
 drop table data_1
 go
 create table data_1(
 uid varchar(50),
 appid int,
 app_type varchar(50),
 start_time varchar(50),
 end_time varchar(50),
 duration varchar(50),
 up_flow varchar(50),
 down_flow varchar(50)
 )--导入所有数据并合并所有数据--时间转换
update data_1 set start_time = DateDiff(s,'00:00:00',start_time)
 update data_1 set end_time = DateDiff(s,'00:00:00',end_time)--6. app 系统类别转码 0- 1
 update data_1 set app_type =
 case when app_type = 'sys'
 then 0
 else 1
 end--更新数据
update data_1 set [uid] = id from data_1 a join [uid_1] u on a.[uid]
 = u.UUid
 update data_1 set appid = id from data_1 a join appid_1 b on a.appid
  = b.appid--数据聚合
if object_id('data_11') is not null
 drop table data_11
 go
 SELECT [uid], app_class,app_type, count(duration) app_count,
 avg(cast(start_time as float)) start_time_avg, avg(cast(end_time as
 float)) end_time_avg, SUM(cast(duration as bigint)) duration_sum,
 avg(cast(duration as float)) duration_avg,
 sum(cast(up_flow as bigint)) as up_flow_sum, sum(cast(down_flow as
 bigint)) as down_flow_sum, avg(cast(up_flow as float)) up_flow_avg,
 avg(cast(down_flow as float)) down_flow_avg
 INTO data_11
 FROM data_1 a left join app_class b on a.appid = b.appid
 GROUP BY [uid],b.app_class,app_type```



