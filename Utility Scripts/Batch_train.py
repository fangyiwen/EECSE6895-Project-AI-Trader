import requests
import threading
import datetime


def auto_update():
    print(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3])

    root_url = "http://127.0.0.1:8000/aitrader"

    # ticker_list = ['600519.SS', '601398.SS', '601318.SS', '601939.SS',
    #                '600036.SS', '000858.SS', '601288.SS', '601988.SS',
    #                '601628.SS', '300750.SS', '601857.SS', '000333.SS',
    #                '300999.SS', '603288.SS', '002415.SS', '601888.SS',
    #                '600276.SS', '300760.SS', '600028.SS', '002594.SS',
    #                '601166.SS', '600900.SS', '002352.SS', '000001.SS',
    #                '688981.SS', '601658.SS', '601012.SS', '603259.SS',
    #                '000568.SS', '002475.SS', '600309.SS', '002714.SS',
    #                '601088.SS', '000651.SS', '600031.SS', '601328.SS',
    #                '600030.SS', '300015.SS', '601601.SS', '600809.SS',
    #                '300059.SS', '000002.SS', '002304.SS', '600690.SS',
    #                '600000.SS', '601138.SS', '601066.SS', '600887.SS',
    #                '600346.SS', '600104.SS', '601816.SS', '601633.SS',
    #                '300122.SS', '603501.SS', '600585.SS', '002607.SS',
    #                '601319.SS', '601998.SS', '002142.SS', '002493.SS',
    #                '000725.SS', '600438.SS', '600016.SS', '601995.SS',
    #                '300014.SS', '601899.SS', '601818.SS', '601668.SS',
    #                '600999.SS', '688111.SS', '000661.SS', '601766.SS',
    #                '600436.SS', '000538.SS', '600048.SS', '600893.SS',
    #                '300433.SS', '300124.SS', '000895.SS', '002027.SS',
    #                '600019.SS', '601100.SS', '002460.SS', '688036.SS',
    #                '601688.SS', '600588.SS', '300347.SS', '600009.SS',
    #                '300274.SS', '300413.SS', '601211.SS', '600837.SS',
    #                '000708.SS', '600745.SS', '601336.SS', '603392.SS',
    #                '600406.SS', '600703.SS', '000063.SS', '601919.SS']

    ticker_list = ['600519.SS', '601398.SS', '601318.SS', '601939.SS',
                   '600036.SS', '000858.SS', '601288.SS', '601988.SS',
                   '601628.SS', '300750.SS', '601857.SS', '000333.SS']

    # add_stock_list = ['600276.SS', '600028.SS']

    def train_helper(ticker, model):
        requests.get(url=root_url + "/train_" + model + "/" + ticker + "/")

    for ticker in ticker_list:
        threading.Thread(target=train_helper, args=(ticker, 'lstm')).start()
        threading.Thread(target=train_helper, args=(ticker, 'svm')).start()
        threading.Thread(target=train_helper, args=(ticker, 'arima')).start()
        print("Training " + ticker + ": LSTM, SVM, ARIMA")


auto_update()
