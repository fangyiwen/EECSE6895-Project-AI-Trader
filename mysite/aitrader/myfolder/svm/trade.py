# coding:utf-8
import csv


def maxProfit(stockcode):
    # prediction_result=str(stockcode)+'//solution//prediction_result.txt'
    prediction_result = './aitrader/myfolder/svm/' + str(stockcode) + '/solution/prediction_result.txt'
    f=open(prediction_result, encoding="utf-8")
    text = f.read()
    trends=text.strip().split("\t")
    print(trends)
    
    operations=[]
    
    
    for i in range(0, len(trends)-1):
        if round(float(trends[i+1]))>=0 and operations.count("buy")>operations.count("sell"):
            operations.append("hold")
        elif round(float(trends[i+1]))>0 and operations.count("buy")==operations.count("sell"):
            operations.append("buy")
        elif round(float(trends[i+1]))<0 and operations.count("buy")>operations.count("sell"):
            operations.append("sell")
        elif round(float(trends[i]))<0 and operations.count("buy")==operations.count("sell"):
            operations.append("hold")
    
    if operations.count("buy")==operations.count("sell"):
        operations.append("hold")
    elif operations.count("buy")>operations.count("sell"):
        operations.append("sell")
    
    
    list=[["day1", "day2", "day3", "day4", "day5"],operations]
    # solution_path=str(stockcode)+'//solution//solution.csv'
    solution_path = './aitrader/myfolder/svm/' + str(stockcode) + '/solution/solution.csv'
    f = open(solution_path,'w',newline='')
    writer = csv.writer(f)
    for i in list:
        writer.writerow(i)
    f.close()

    return operations



