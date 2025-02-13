import pandas as pd
import csv
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

# 加载数据
def load_data(filename):
    data = pd.read_csv(filename)
    return data

# 按uid分组并计算总流量
def calculate_total_flow(data):
    total_flow = data.groupby('uid')[['up_flow', 'down_flow']].sum().reset_index()
    total_flow['total_flow'] = total_flow['up_flow'] + total_flow['down_flow']
    return total_flow

# 拟合ARIMA模型并进行预测
def fit_arima_model(train_data, test_data):
    # 训练集
    train_values = train_data['total_flow'].values
    model = ARIMA(train_values, order=(1, 0, 0))
    model_fit = model.fit()

    # 绘制ACF和PACF图
    fig, ax = plt.subplots(figsize=(12, 4))
    plot_acf(train_values, ax=ax, lags=15)
    plt.xlabel('Lag')
    plt.ylabel('Autocorrelation')
    plt.title('Autocorrelation Function (ACF)')
    plt.ylim(-0.3, 0.3)  # 设置Autocorrelation图的y轴范围
    plt.show()
    plt.show()

    fig, ax = plt.subplots(figsize=(12, 4))
    plot_pacf(train_values, ax=ax, lags=15, method='ywmle')
    plt.xlabel('Lag')
    plt.ylabel('Partial Autocorrelation')
    plt.title('Partial Autocorrelation Function (PACF)')
    plt.ylim(-0.3, 0.3)  # 设置Partial Autocorrelation图的y轴范围
    plt.show()

    # 预测
    start = len(train_values)
    end = start + len(test_data) - 1
    preds = model_fit.predict(start=start, end=end)

    return preds

# 计算准确率
def calculate_accuracy(actual, predicted):
    actual_labels = [1 if value > 0 else 0 for value in actual]
    predicted_labels = [1 if value > 0 else 0 for value in predicted]
    accuracy = accuracy_score(actual_labels, predicted_labels)
    return accuracy

# 主函数
def main():
    # 训练集和测试集文件路径
    train_files = ['./a类数据/train{:02d}.csv'.format(i) for i in range(1, 12)]
    test_files = ['./a类数据/test{:02d}.csv'.format(i) for i in range(12, 22)]

    accuracies = [] # 准确率列表

    for idx, (train_file, test_file) in enumerate(zip(train_files, test_files)):
        # 加载训练集和测试集数据
        train_data = load_data(train_file)
        test_data = load_data(test_file)

        # 计算总流量
        train_total_flow = calculate_total_flow(train_data)
        test_total_flow = calculate_total_flow(test_data)

        # 拟合ARIMA模型并进行预测
        preds = fit_arima_model(train_total_flow, test_total_flow[['total_flow']])

        # 计算准确率
        accuracy = calculate_accuracy(test_total_flow['total_flow'], preds)
        accuracies.append(accuracy)

        print("预测结果：", preds)
        print("真实结果：", test_total_flow['total_flow'])
        print("准确率：", accuracy)

        # 将预测结果和真实结果存储到文件中
        result_df = pd.DataFrame({'预测结果': preds, '真实结果': test_total_flow['total_flow']})
        result_df.to_csv('jg{:02d}.csv'.format(idx + 1), index=False, encoding='utf-8-sig', quoting=csv.QUOTE_NONNUMERIC)

    average_accuracy = sum(accuracies) / len(accuracies)
    print("平均准确率：", average_accuracy)

if __name__ == '__main__':
    main()
