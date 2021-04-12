# coding:utf-8
import csv
import os

root_path = "./aitrader/myfolder/"


def ModelsTrade(stockcode):
    LSTM_result = root_path + 'lstm//' + str(
        stockcode) + '//solution//prediction_result.txt'
    SVM_result = root_path + 'svm//' + str(stockcode) + '//solution//prediction_result.txt'
    ARIMA_result = root_path + 'arima//' + str(
        stockcode) + '//solution//prediction_result.txt'
    solution_path = root_path + 'integration//' + str(
        stockcode) + '//solution//solution_3models.csv'

    def GetTrends(file_path):
        trends = []
        f = open(file_path, encoding="utf-8")
        lines = f.readlines()
        prices = lines[0].strip().split("\t")
        trends.append(int(lines[1]))

        for i in range(1, len(prices)):
            if prices[i] > prices[i - 1]:
                trends.append(int("1"))
            elif prices[i] == prices[i - 1]:
                trends.append(int("0"))
            elif prices[i] < prices[i - 1]:
                trends.append(int("-1"))

        return trends

    trends_LSTM = GetTrends(LSTM_result)

    f_SVM = open(SVM_result, encoding="utf-8")
    text_SVM = f_SVM.read()
    trends_SVM = text_SVM.strip().split("\t")

    trends_ARIMA = GetTrends(ARIMA_result)

    day = 0
    final_Trend = []

    while (day < 5):
        temp = []
        temp.append(trends_LSTM[day])
        temp.append(round(float(trends_SVM[day])))
        temp.append(trends_ARIMA[day])

        output = 0
        if temp.count(1) > temp.count(-1):
            if temp.count(1) > temp.count(0):
                output = 1
            elif temp.count("1") < temp.count(0):
                output = 0
        elif temp.count(-1) > temp.count(1):
            if temp.count(-1) > temp.count(0):
                output = -1
            elif temp.count(-1) < temp.count(0):
                output = 0
        final_Trend.append(output)
        day = day + 1

    operations = []

    for i in range(0, len(final_Trend) - 1):
        if final_Trend[i + 1] >= 0 and operations.count(
                "buy") > operations.count("sell"):
            operations.append("hold")
        elif final_Trend[i + 1] > 0 and operations.count(
                "buy") == operations.count("sell"):
            operations.append("buy")
        elif final_Trend[i + 1] < 0 and operations.count(
                "buy") > operations.count("sell"):
            operations.append("sell")
        elif final_Trend[i] < 0 and operations.count("buy") == operations.count(
                "sell"):
            operations.append("hold")
        else:
            operations.append("hold")

    if operations.count("buy") == operations.count("sell"):
        operations.append("hold")
    elif operations.count("buy") > operations.count("sell"):
        operations.append("sell")

    list = [["day1", "day2", "day3", "day4", "day5"], operations]

    isExists = os.path.exists(root_path + 'integration//' + str(stockcode) + '//solution')
    if not isExists:
        os.makedirs(root_path + 'integration//' + str(stockcode) + '//solution')

    # solution_path='ARIMA//'+str(stockcode)+'//solution//solution_3models.csv'

    f = open(solution_path, 'w', newline='')
    writer = csv.writer(f)
    for i in list:
        writer.writerow(i)
    f.close()

    return trends_LSTM, trends_SVM, trends_ARIMA, final_Trend, operations

# ModelsTrade(600519)
