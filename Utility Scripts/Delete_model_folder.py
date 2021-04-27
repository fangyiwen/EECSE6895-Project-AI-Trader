import os
import shutil

path = "../mysite/aitrader/myfolder/lstm"
files = os.listdir(path)

for file in files:
    file_path = path + '/' + file
    if not (file == 'lstm_model.py' or file == 'trade.py'):
        if os.path.isdir(file_path):
            shutil.rmtree(file_path)
        if os.path.isfile(file_path):
            os.remove(file_path)

path = "../mysite/aitrader/myfolder/svm"
files = os.listdir(path)

for file in files:
    file_path = path + '/' + file
    if not (file == 'SVM_model.py' or file == 'trade.py'):
        if os.path.isdir(file_path):
            shutil.rmtree(file_path)
        if os.path.isfile(file_path):
            os.remove(file_path)

path = "../mysite/aitrader/myfolder/arima"
files = os.listdir(path)

for file in files:
    file_path = path + '/' + file
    if not (file == 'ARIMA_model.py' or file == 'trade.py'):
        if os.path.isdir(file_path):
            shutil.rmtree(file_path)
        if os.path.isfile(file_path):
            os.remove(file_path)

print('Deleting finished')
