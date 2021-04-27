import requests
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import time
import os
import sys
import multiprocessing

sys.path.append(os.path.abspath('../mysite/aitrader/myfolder/code'))
sys.path.append(os.path.abspath('../mysite/aitrader/myfolder'))
from data_download import data_download
from data_download_with_date import data_download_with_date
from lstm.lstm_model import run_lstm_model
from svm.SVM_model import train_SVM_model
from arima.ARIMA_model import train_ARIMA_model


# pip install APScheduler

def train_helper(ticker, model):
    if model == 'lstm':
        data_download(ticker, model, invoke_from_http=False)
        run_lstm_model(ticker[:-3], invoke_from_http=False)
    elif model == 'svm':
        data_download(ticker, model, invoke_from_http=False)
        train_SVM_model(ticker[:-3], invoke_from_http=False)
    elif model == 'arima':
        data_download_with_date(ticker, model, invoke_from_http=False)
        train_ARIMA_model(ticker[:-3], invoke_from_http=False)


# pip install APScheduler

if __name__ == '__main__':
    def auto_update():
        print("Number of processors: ", multiprocessing.cpu_count())
        print(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3])

        start = time.time()

        root_url = "http://127.0.0.1:8000/aitrader"

        URL = root_url + "/" + "stock_all/"
        r = requests.get(url=URL)
        data = r.json()
        ticker_list = data["ticker_list"]

        # pool = multiprocessing.Pool(processes=6)
        pool = multiprocessing.Pool()

        for ticker in ticker_list:
            pool.apply_async(train_helper, (ticker, 'lstm'))
            pool.apply_async(train_helper, (ticker, 'svm'))
            pool.apply_async(train_helper, (ticker, 'arima'))
            print("Training " + ticker + ": LSTM, SVM, ARIMA")

        pool.close()
        pool.join()

        end = time.time()
        print('Start:', start)
        print('End:', end)
        print('Running time:', end - start)


    # Auto schedule
    scheduler = BlockingScheduler()
    scheduler.add_job(
        auto_update,
        trigger='cron',
        second=0,
        minute=30,
        hour=15,
        timezone="Asia/Shanghai"
    )
    scheduler.start()

    # auto_update()
