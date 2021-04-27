import requests
import threading
import datetime


def auto_update():
    print(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3])

    root_url = "http://127.0.0.1:8000/aitrader"

    # ticker_list = ['600519.SS', '601398.SS', '600036.SS', '601288.SS',
    #                '601318.SS', '601988.SS', '601857.SS', '601628.SS',
    #                '601888.SS', '603288.SS', '600000.SS', '600004.SS',
    #                '600006.SS', '600007.SS', '600008.SS', '600009.SS',
    #                '600010.SS', '600011.SS', '600012.SS', '600015.SS']

    ticker_list = ['600519.SS', '601398.SS', '600036.SS', '601288.SS',
                   '601318.SS', '601988.SS', '601857.SS', '601628.SS',
                   '601888.SS', '603288.SS']

    # add_stock_list = ['600012.SS', '600015.SS']

    def train_helper(ticker, model):
        requests.get(url=root_url + "/train_" + model + "/" + ticker + "/")

    for ticker in ticker_list:
        threading.Thread(target=train_helper, args=(ticker, 'lstm')).start()
        threading.Thread(target=train_helper, args=(ticker, 'svm')).start()
        threading.Thread(target=train_helper, args=(ticker, 'arima')).start()
        print("Training " + ticker + ": LSTM, SVM, ARIMA")


auto_update()
