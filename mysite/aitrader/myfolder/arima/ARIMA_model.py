import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima_model import ARIMA
import numpy as np
import os
import json


def train_ARIMA_model(stockcode, invoke_from_http=True):
    root_path = "./aitrader/myfolder/arima/"

    if not invoke_from_http:
        root_path = "../mysite/aitrader/myfolder/arima/"

    # ==============load data===============
    data_path = root_path + str(stockcode) + ".SS.csv"
    # data_path="./"+str(600519)+".SS.csv"
    StockDate = pd.read_csv(data_path)

    StockDate['close'].plot()
    plt.title('Daily closing price')
    plt.show()

    StockDate.index = pd.to_datetime(StockDate['date'])
    print(StockDate)
    stock_week = StockDate['close'].resample('W-MON').mean()

    # train set
    L = len(stock_week)
    train = int(L)
    total_predict_data = L - train

    train_data = stock_week[:train]
    print(train_data)

    train_data.plot()
    plt.title('Average weekly closing price')
    plt.show()

    # first difference
    diff_data = train_data.diff(1).dropna()
    diff_data.plot()
    plt.show()

    # check acf and pacf to make sure of q and p
    acf = plot_acf(diff_data, lags=25)
    plt.title('ACF')
    acf.show()
    pacf = plot_pacf(diff_data, lags=25)
    plt.title('PACF')
    pacf.show()
    plt.show()

    where_are_nan = np.isnan(train_data)
    where_are_inf = np.isinf(train_data)
    train_data[where_are_nan] = 0
    train_data[where_are_inf] = 0

    model = ARIMA(train_data, order=(1, 1, 1), freq='W-MON')
    arima = model.fit()

    # predict_data = arima.predict('2021-03-01',dynamic=True,typ='levels')
    predict_data = arima.forecast(5)
    print(str(predict_data[0]))

    isExists = os.path.exists(root_path + str(stockcode) + '/solution')
    if not isExists:
        os.makedirs(root_path + str(stockcode) + '/solution')

    prediction_result = []
    with open(root_path + str(stockcode) + '/solution/prediction_result.txt',
              'w') as f:
        for item in str(predict_data[0])[1:-1].replace("  ", " ").split(" "):
            print(item)
            f.write(item + "\t")
            if item.strip() != '':
                prediction_result.append(float(item))

        if prediction_result[0] > StockDate['close'][-1]:
            f.write("\n" + "1")
        elif prediction_result[0] == StockDate['close'][-1]:
            f.write("\n" + "0")
        elif prediction_result[0] < StockDate['close'][-1]:
            f.write("\n" + "-1")

    print(prediction_result)

    isExists = os.path.exists(root_path + str(stockcode) + "/figure")
    if not isExists:
        os.makedirs(root_path + str(stockcode) + "/figure")

    plt.figure()
    plt.plot(list(range(len(prediction_result))), prediction_result,
             color='b', )
    plt.xlabel('days', fontsize=14)
    plt.ylabel('close value', fontsize=14)
    plt.title('future 5 days', fontsize=15)
    figurepath_5days = root_path + str(stockcode) + "/figure/future5days.jpg"
    plt.savefig(figurepath_5days)
    plt.show()

    # Save datapoint
    isExists = os.path.exists(
        root_path + str(stockcode) + "/datapoint")
    if not isExists:
        os.makedirs(root_path + str(stockcode) + "/datapoint")
    future5days_path = root_path + str(
        stockcode) + "/datapoint/" + 'future5days' + ".json"

    jsObj = json.dumps([float(x) for x in prediction_result])
    fileObject = open(future5days_path, 'w')
    fileObject.write(jsObj)
    fileObject.close()

# train_ARIMA_model(600519)
