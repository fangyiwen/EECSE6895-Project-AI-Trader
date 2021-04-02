#V2.0 
#change all the data, now it's base on relation not price. 
#Increase the training Data set.
#from yahoo_finance import Share
from pandas import Series,DataFrame
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
import os

def train_SVM_model(stockcode):
    #initialization
    prediction_result=[]
    
    #mk dir
    isExists=os.path.exists(str(stockcode)+'//solution')
    if not isExists:
      os.makedirs(str(stockcode)+'//solution')

    #Data processing
    data_path="./"+str(stockcode)+".SS.csv"
    StockDate = pd.read_csv(data_path)
    

    #Create more data for 5 days.
    n=1
    
    while n<=5:
        Data=StockDate.astype(float)

        print("=====================predicting day", n, "=========================")
        value = pd.Series(Data['close'].shift(-n)-Data['close'],index=Data.index) #after n days, rise or fall
        Data['High-Low'] = Data['high']-Data['low'] #Difference between High and Low
        Data['Open-NClose']=Data['open']-Data['close'].shift(n) #today's open - close of n days before
        Data['Close-NClose']=Data['close']-Data['close'].shift(n) #Today is rise or fall comparing with n days before
        Data['Close-Open']=Data['close']-Data['open'] #today's Close - Open
        Data['High-Close'] = Data['high']-Data['close'] #today's High - Close
        Data['Close-Low'] = Data['close']-Data['low'] #today's Close - Low
        value[value>0]=1 #1 means rise
        value[value==0]=0 #0 means it doesn't rise or fall
        value[value<0]=-1 #-1 means fall
        Data=Data.dropna(how='any')
        del(Data['open'])
        del(Data['close'])
        del(Data['high'])
        del(Data['low'])
        print(Data)
        #print(type(Data))
        Data['Value']=value
        
        L=len(Data)
        train = int(0.9*L)  #How many data for train, 9 is the least.
        total_predict_data=L-train

        DATA_lastday_prediction=Data.tail(1)
        DATA_lastday_prediction['Value']=0
        print(DATA_lastday_prediction)

        correct = 0
        
        #loop training,30 days data for training
        
        i=0
        flag=0
        SampleSize=30
        print("SampleSize: ", SampleSize)
        print("There will be %d loops." % min(train//SampleSize, total_predict_data))
        
        while i+SampleSize<train & train<L:
            Data_train = Data[i+n:i+n+SampleSize]
            value_train = value[i+n:i+n+SampleSize]
            
            Data_predict = Data[train:train+1]
            value_real = value[train:train+1]
            
            print(Data_predict)
            #print(value_train)
            print("===============", flag+1, "loop===============")
            classifier = svm.SVC(kernel='poly',degree=20)  #kernel='poly',(gamma*u'*v + coef0)^degree
            classifier.fit(Data_train,value_train)
            
            value_predict=classifier.predict(Data_predict)

            a = str(value_real).strip().split(".")[0][-1]
            b = str(value_real).strip().split(".")[1][0]
            value_real = float(a+"."+b)
            
            print("value_real: ", value_real)
            print("value_predict: ", value_predict)
            if(int(value_real)==int(value_predict)):
                correct=correct+1
            i = i+SampleSize
            flag=flag+1
            train=train+1
        
        correct=correct/flag*100
        print("Correct= %.4f" % correct)
        n=n+1

        prediction_result.append(classifier.predict(DATA_lastday_prediction))


    with open(str(stockcode)+'//solution//prediction_result.txt','w') as f:
      for item in prediction_result:
        f.write(str(item)[1:-1]+"0\t")
    

    
    isExists=os.path.exists(str(stockcode)+"//figure")
    if not isExists:
      os.makedirs(str(stockcode)+"//figure")

    plt.figure()
    plt.plot(list(range(len(prediction_result))), prediction_result, color='b', )
    plt.xlabel('days', fontsize=14)
    plt.ylabel('close value', fontsize=14)
    plt.title('future 5 days '+' 1:rise, -1:fall', fontsize=15)
    figurepath_5days=str(stockcode)+"//figure//future5days.jpg"
    plt.savefig(figurepath_5days)
    plt.show()

