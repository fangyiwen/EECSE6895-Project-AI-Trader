from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from yahoo_fin.stock_info import get_data, get_quote_data
from aitrader.myfolder.lstm.trade import maxProfit as maxProfit_lstm
import os
import datetime
from aitrader.myfolder.svm.trade import maxProfit as maxProfit_svm

# Create your views here.

def index(request):
    context = {'context': "You're looking"}
    return render(request, 'aitrader/index.html', context)


def select_stock(request):
    ticker_list = ['600519.SS',
                   '601398.SS',
                   '600036.SS',
                   '601288.SS',
                   '601318.SS',
                   '601857.SS',
                   '601988.SS',
                   '601628.SS',
                   '601888.SS',
                   '603288.SS'
                   ]

    class TickerObj:
        def __init__(self, ticker, longName):
            self.ticker = ticker
            self.longName = longName

    sticker_obj_list = []
    for ticker in ticker_list:
        tmp = TickerObj(ticker, get_quote_data(ticker)['longName'])
        sticker_obj_list.append(tmp)

    context = {'sticker_obj_list': sticker_obj_list}
    return render(request, 'aitrader/select_stock.html', context)


def trade_stock_lstm(request, stock_id):
    if request.method == 'GET':
        context = {'stock_id': stock_id,
                   'longName': get_quote_data(stock_id)['longName']}

        return render(request, 'aitrader/trade_stock_lstm.html', context)
    elif request.method == 'POST':
        initial_balance = request.POST['initial_balance']
        url = '/aitrader/trade_run_lstm/' + stock_id + '/' + initial_balance + '/'

        return HttpResponseRedirect(url)


def trade_stock_svm(request, stock_id):
    if request.method == 'GET':
        context = {'stock_id': stock_id,
                   'longName': get_quote_data(stock_id)['longName']}

        return render(request, 'aitrader/trade_stock_svm.html', context)
    elif request.method == 'POST':
        url = '/aitrader/trade_run_svm/' + stock_id + '/'

        return HttpResponseRedirect(url)

def trade_run_lstm(request, stock_id, initial_balance):
    stock_id_number_only = stock_id[:-3]
    tmp = maxProfit_lstm(stock_id_number_only, int(initial_balance))
    operations, week_profit, balance = tmp

    path = "./aitrader/myfolder/lstm/" + stock_id_number_only + "/figure"
    files = os.listdir(path)
    figure_list = []
    for file in files:
        if file[:3] == "day":
            figure_list.append(file)
    figure_list.sort(key=lambda x: int(x[3:-4]))

    date_list = []
    for i in range(len(operations)):
        date = findComingMonday() + datetime.timedelta(days=i)
        date_list.append(date.strftime('%Y-%m-%d'))

    date_operations_dict = {date_list[i]: operations[i] for i in
                            range(len(operations))}

    context = {'stock_id': stock_id,
               'stock_id_number_only': stock_id_number_only,
               'longName': get_quote_data(stock_id)['longName'],
               'initial_balance': initial_balance,
               'week_profit': round(week_profit),
               'balance': round(balance),
               'figure_list': figure_list,
               'date_operations_dict': date_operations_dict
               }
    return render(request, 'aitrader/trade_run_lstm.html', context)


def trade_run_svm(request, stock_id):
    stock_id_number_only = stock_id[:-3]
    tmp = maxProfit_svm(stock_id_number_only)
    operations = tmp

    path = "./aitrader/myfolder/svm/" + stock_id_number_only + "/figure"
    files = os.listdir(path)
    figure_list = []
    for file in files:
        if file[:11] == "future5days":
            figure_list.append(file)

    date_list = []
    for i in range(len(operations)):
        date = findComingMonday() + datetime.timedelta(days=i)
        date_list.append(date.strftime('%Y-%m-%d'))

    date_operations_dict = {date_list[i]: operations[i] for i in
                            range(len(operations))}

    context = {'stock_id': stock_id,
               'stock_id_number_only': stock_id_number_only,
               'longName': get_quote_data(stock_id)['longName'],
               'figure_list': figure_list,
               'date_operations_dict': date_operations_dict
               }
    return render(request, 'aitrader/trade_run_svm.html', context)

# Helper
def findComingMonday():
    today = datetime.date.today()
    coming_monday = today + datetime.timedelta(days=-today.weekday(), weeks=1)
    return coming_monday
