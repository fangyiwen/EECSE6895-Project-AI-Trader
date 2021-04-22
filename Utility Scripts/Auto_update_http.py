import requests
import threading
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler


# pip install APScheduler

def auto_update():
    print(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3])

    root_url = "http://127.0.0.1:8000/aitrader"

    URL = root_url + "/" + "stock_all/"
    r = requests.get(url=URL)
    data = r.json()
    ticker_list = data["ticker_list"]

    def train_helper(ticker, model):
        requests.get(url=root_url + "/train_" + model + "/" + ticker + "/")

    for ticker in ticker_list:
        threading.Thread(target=train_helper, args=(ticker, 'lstm')).start()
        threading.Thread(target=train_helper, args=(ticker, 'svm')).start()
        threading.Thread(target=train_helper, args=(ticker, 'arima')).start()
        print("Training " + ticker + ": LSTM, SVM, ARIMA")


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
