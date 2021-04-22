from yahoo_fin.stock_info import get_data


def data_download_with_date(stock_id, model, invoke_from_http=True):
    root_path = "./aitrader/myfolder/"

    if not invoke_from_http:
        root_path = "../mysite/aitrader/myfolder/"

    ticker = stock_id
    # ticker = '600519.SS'
    stock = get_data(ticker, start_date=None, end_date=None,
                     index_as_date=False, interval="1d")
    stock.dropna(axis=0, how='any', inplace=True)
    print(stock[len(stock) - 5:len(stock)])

    latest_date = stock.iloc[len(stock) - 1, 0].strftime('%Y-%m-%d')
    print(latest_date)

    stock.drop(labels=['ticker', 'adjclose', 'volume'], axis=1,
               inplace=True)
    order = ['date', 'open', 'high', 'low', 'close']
    stock = stock[order]

    stock.to_csv(root_path + model + '/' + ticker + '.csv', index=None)
    f = open(root_path + model + '/' + ticker + "_latest_date.txt", "w")
    f.write(latest_date)
    f.close()

# data_download('600519.SS', 'lstm')
