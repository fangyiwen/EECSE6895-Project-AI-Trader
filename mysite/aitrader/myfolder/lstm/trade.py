# coding:utf-8
import csv


def maxProfit(stockcode, balance):
    root_path = "./aitrader/myfolder/lstm/"

    # prediction_result=str(stockcode)+'//solution//prediction_result.txt'
    prediction_result = root_path + str(
        stockcode) + '/solution/prediction_result.txt'
    f = open(prediction_result, encoding="utf-8")
    lines = f.readlines()
    prices = lines[0].strip().split("\t")
    print(prices)
    operations = ["hold"] * len(prices)

    profit = 0
    for i in range(0, len(prices) - 1):
        if float(prices[i + 1]) >= float(prices[i]):
            profit = profit + float(prices[i + 1]) - float(prices[i])
            if operations.count("buy") > operations.count("sell"):
                operations[i] = "hold"
            elif operations.count("buy") == operations.count(
                    "sell") and balance >= float(prices[i]) * 100:
                operations[i] = "buy"
        elif float(prices[i + 1]) < float(prices[i]):
            if operations.count("buy") > operations.count("sell"):
                operations[i] = "sell"
            elif operations.count("buy") == operations.count("sell"):
                operations[i] = "hold"

    if operations[-1] == "hold" and operations.count("buy") > operations.count(
            "sell"):
        operations[-1] = "sell"

    week_profit = float(balance // (float(prices[i]) * 100)) * profit * 100
    print(week_profit, balance + week_profit)
    print(operations)

    list = [["day1", "day2", "day3", "day4", "day5"], prices, operations]
    # solution_path=str(stockcode)+'/solution/solution.csv'
    solution_path = root_path + str(stockcode) + '/solution/solution.csv'
    f = open(solution_path, 'w', newline='')
    writer = csv.writer(f)
    for i in list:
        writer.writerow(i)
    f.close()

    return operations, week_profit, balance + week_profit
