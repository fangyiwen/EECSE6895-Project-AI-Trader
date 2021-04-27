import datetime
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


if __name__ == '__main__':
    def auto_update():
        print("Number of processors: ", multiprocessing.cpu_count())
        print(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3])

        start = time.time()

        # ticker_list = ['600519.SS', '601398.SS', '600036.SS', '601288.SS',
        #                '601318.SS', '601988.SS', '601857.SS', '601628.SS',
        #                '601888.SS', '603288.SS', '600000.SS', '600004.SS',
        #                '600006.SS', '600007.SS', '600008.SS', '600009.SS',
        #                '600010.SS', '600011.SS', '600012.SS', '600015.SS']

        ticker_list = ['600519.SS', '601398.SS', '600036.SS', '601288.SS',
                       '601318.SS', '601988.SS', '601857.SS', '601628.SS',
                       '601888.SS', '603288.SS']

        # ticker_list = ['600519.SS', '601398.SS']

        # add_stock_list = ['600012.SS', '600015.SS']

        pool = multiprocessing.Pool(processes=3)
        # pool = multiprocessing.Pool()

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


    auto_update()
