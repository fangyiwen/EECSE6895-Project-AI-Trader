import requests
import threading
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import time
import os
import sys

sys.path.append(os.path.abspath('../mysite/aitrader/myfolder/code'))
sys.path.append(os.path.abspath('../mysite/aitrader/myfolder'))
from data_download import data_download
from data_download_with_date import data_download_with_date
from lstm.lstm_model import run_lstm_model
from svm.SVM_model import train_SVM_model
from arima.ARIMA_model import train_ARIMA_model


# pip install APScheduler

def auto_update():
    print(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3])

    start = time.time()
    threads_list = []

    root_url = "http://127.0.0.1:8000/aitrader"

    URL = root_url + "/" + "stock_all/"
    r = requests.get(url=URL)
    data = r.json()
    ticker_list = data["ticker_list"]

    def train_helper(ticker, model):
        if model == 'lstm':
            data_download(ticker, model, invoke_from_http=False)
            run_lstm_model(ticker[:-3], invoke_from_http=False)
        # elif model == 'svm':
        #     data_download(ticker, model, invoke_from_http=False)
        #     train_SVM_model(ticker[:-3], invoke_from_http=False)
        # elif model == 'arima':
        #     data_download_with_date(ticker, model, invoke_from_http=False)
        #     train_ARIMA_model(ticker[:-3], invoke_from_http=False)

    for ticker in ticker_list:
        th = threading.Thread(target=train_helper, args=(ticker, 'lstm'))
        th.start()
        th2 = threading.Thread(target=train_helper, args=(ticker, 'svm'))
        th2.start()
        th3 = threading.Thread(target=train_helper, args=(ticker, 'arima'))
        th3.start()
        threads_list.append(th)
        threads_list.append(th2)
        threads_list.append(th3)
        print("Training " + ticker + ": LSTM, SVM, ARIMA")

    for t in threads_list:
        t.join()

    end = time.time()
    print('Start:', start)
    print('End:', end)
    print('Running time:', end - start)


# Auto schedule
# scheduler = BlockingScheduler()
# scheduler.add_job(
#     auto_update,
#     trigger='cron',
#     second=0,
#     minute=30,
#     hour=15,
#     timezone="Asia/Shanghai"
# )
# scheduler.start()

auto_update()
