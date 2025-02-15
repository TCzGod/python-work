# python-work
大学期间做的部分python项目
## 基于多模态机器学习的移动用户行为分析与预测系统
系统主要解决以下问题：
问题 1：结合多种模型方法，选择合理的聚类数量，根据用户常用所属的20类APP的数据进行
聚类，并对结果进行比较分析；
问题 2：根据问题1得到的分析结果，对不同的用户进行用户画像处理，并描述不同用户的属
性特征；
问题 3：根据用户第1~11天的a类APP的使用情况，来预测用户在第12~21天是否会使用该类
APP，并给出预测结果的准确率；
问题 4：根据用户第1~11天的a类APP的使用情况，来预测用户在第12~21天使用a类APP的有
效日均使用时长，并计算评价指标NMSE。
<img width="141" alt="31" src="https://github.com/user-attachments/assets/e90ab6ac-3a56-42f5-890a-cb14b60cdb3a" />
整个系统设计流程图
<img width="481" alt="12" src="https://github.com/user-attachments/assets/78938a4b-8c4f-4925-b330-549d6d5e345a" />
前期数据分析与处理
### 数据分析
①Pearson、Spearman 相关性矩阵
<img width="573" alt="11" src="https://github.com/user-attachments/assets/30faa57b-96c5-4da5-bf83-74afb85074d3" />
②特征变量散点分布图
<img width="587" alt="10" src="https://github.com/user-attachments/assets/527d3ddd-8652-40d2-bce5-848258f0d57c" />
### 数据处理
①时间转换
对start_time与end_time 特征转换为一天当中的秒数，为无符号整数，方便模型的计算
②去量纲化
up_flow 与 down_flow 是用户检测数据中每条样本的总计，为了提高模型的可解释性，
本文计算了每条样本每秒的上行流量与下行流量，即：
<img width="380" alt="9" src="https://github.com/user-attachments/assets/09f95f71-0965-4d71-90f5-97dcb1daac55" />
并计算上行流量与下行流量之间的差异作为样本特征。
③数据合并与连接
将用户day01至day21的所有经过处理的检测数据进行合并，方便数据的读取与处理，并将
用户检测数据与app类别数据进行左连接合并在一起，作为特征数据。
④数据编码
对uid、appid、app_class 特征进行编码。为数据样本太多，本文没有采用One-Hot编码，
使用了LabelEnCoder 编码，将类别数据或唯一标识数据转化为连续性的整数编号，防止离
散数据影响模型的计算结果。
⑤数据聚合
因源数据量过于庞大，本文对齐进行聚合处理，产生新的数据集，根据uid和appid进行聚合，
uid为第一分组特征，appid为第二分组特征，统计每一个用户检测样本中每一个app的特征。
根据聚类结果对用户进行画像
<img width="549" alt="7" src="https://github.com/user-attachments/assets/dd3b5bae-58eb-41ce-bda5-36456a0599d1" />
①类别一用户：
数据基数为21842239，app平均使用频次前三类别f、p、t(362、68、63),
 app 平均使用时间前三类h、f、b(390079、230838、118321),单位：秒，
平均上行流量前三类：f、c、g(246、216、122)，单位：MB
平均下行流量前三类：c、o、f(78、65、12),单：位MB
 ②类别二用户：
数据基数为35806，app平均使用频次前三类别g、o、c(1279、995、189),
 app 平均使用时间前三类g、c、o(381578、200713、111071),单位：秒，
平均上行流量前三类：o、g、c(26966、22685、19125)，单位：MB
平均下行流量前三类：c、g、t(13342、11164、8182),单：位MB
③类别三用户：
数据基数为239398，app平均使用频次前三类别f、h、p(1359、998、575),
 app 平均使用时间前三类j、f、c(213232、185731、183739),单位：秒，
平均上行流量前三类：h、q、g(12245、8533、8364)，单位：MB
平均下行流量前三类：e、o、c(4720、3844、3811),单：位MB
 ④类别四用户：
数据基数为3387719，app平均使用频次前三类别f、p、a(1009、415、337),
 app 平均使用时间前三类f、g、t(127939、96821、92457),单位：秒，
平均上行流量前三类：s、t、c(2420、2349、2327)，单位：MB
平均下行流量前三类：o、c、t(1123、941、478),单：位MB
综述：
用户在下午2-3点使用app频次最高。
用户使用系统自带app频次较少，使用用户安装app频次占大多数。
## ARIMA模型对用户行为预测
基本步骤
Step1:输入与用户使用A类软件相关的数据；
Step2:对收集到的数据进行预处理，包括数据清洗、缺失值处理、异常值处理等，确保
数据的质量和完整性；
Step3:将预处理后的数据按照时间顺序排列，形成时间序列数据；
Step4:根据数据的性质选择合适的ARIMA模型参数。通过观察自相关图（ACF）和偏自
相关图（PACF）来确定自回归阶数（w）、差分阶数（a）和移动平均阶数（d）；
Step5:使用选定的ARIMA模型参数对时间序列数据进行模型训练；
Step6:使用验证数据集对训练好的ARIMA模型进行验证；
Step7:使用训练好的ARIMA模型进行未来用户是否会继续使用A类软件的预测
Step8:输出结果
拟合结果
<img width="457" alt="6" src="https://github.com/user-attachments/assets/be508999-59f7-432b-9e9d-675e0c94535e" />
## 随机森林对用户使用时长的预测
随机森林的基本步骤
Step1:输入与用户使用A类软件相关的数据；
Step2:对收集到的数据进行预处理，包括数据清洗、缺失值处理、异常值处理等，确保
数据的质量和完整性；
Step3:将预处理后的数据集划分为训练集和测试集；
Step4:使用训练集来构建随机森林模型。随机森林由多个决策树组成，在每个决策树中
随机选择特征进行分裂，最后通过投票或平均预测结果来确定最终的预测值；
Step5:使用训练集对随机森林进行训练，调整模型参数以提高预测准确率。通过反复迭
代优化来找到最佳的模型参数组合；
Step6:使用测试集对训练好的模型进行评估，计算预测结果与实际结果之间的误差（例
如使用平均绝对误差MAE或均方根误差RMSE）；
Step7:输出结果。
<img width="503" alt="5" src="https://github.com/user-attachments/assets/75a1a8df-4b6f-4666-b786-8f8b0a9f4cd5" />
其中涉及到的sql代码
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



