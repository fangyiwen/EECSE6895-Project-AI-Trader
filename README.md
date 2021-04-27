# EECSE6895 Project: A-share Stock Auto Trader
B9: Investment Strategy - AI Trader (CN/HK/TW/JP)

## Introduction
The financial market is one of the first to adopt machine learning. Since the 1980s, people have been using machine learning to discover the laws of the financial market. Although machine learning has achieved great success in forecasting in other fields, the stock market is a market where everyone can invest in profit, but machine learning forecasts have not achieved significant results. As stock traders, we want to simulate stock prices or its trend correctly so that we can reasonably decide when to buy stocks and when to sell stocks in order to achieve maximum profitability. In this project, we will deploy LSTM, SVM, ARIMA methods to train models, then predict stock values or its trends. According to the result, we will design an algorithm to buy it at a low price, sell it at a high price, to achieve profits as much as possible. Finally, we will build a web application visualizing the result, which makes it more intuitive and easier to use and to accept for users.

Visit the deployed website at http://ec2-34-207-212-22.compute-1.amazonaws.com/aitrader/

## Team
Yiwen Fang (yf2560) | Guoshiwen Han (gh2567)

## System Overview
![System Overview](Utility%20Scripts/system_overview.jpg)

## Environment Setup
The command is for local machine. The environment setup for AWS EC2 can be done in a similar way by using ```python3-venv```.

- Upgrade/replace the API key at stockdio.com if the real-time market info fails to show.
- Install Python with the version 3.8.8
- Make a conda virtual environment
    - conda activate my-django
- Install required dependencies (manual way)
    - ```pip install Django==3.1.7```
    - ```pip install yahoo-fin```
    - ```pip install django-bootstrap4```
    - ```pip install matplotlib```
    - ```pip install grpcio==1.27.2```
    - ```pip install tensorflow```
    - ```pip install numpy```
    - ```pip install pandas```
    - ```pip install scikit-learn```
    - ```pip install statsmodels```
- Install required dependencies (lazy way)
    - ```pip install -r requirements.txt```

## Run the Application (Local Machine)
There are two components for the application. Django hosts the frontend and backend. Auto update script triggers the auto downloading and model retraining in a setting period.

- Run Django
    - cd to the directory of "mysite"
    - ```conda activate my-django```
    - ```python manage.py runserver --insecure```
- Run auto update script
    - cd to the directory of "Utility Scripts"
    - ```conda activate my-django```
    - ```conda install pywin32``` (when required)
    - ```python Auto_update.py```

## Run the Application (AWS EC2)
Install screen in Ubuntu ```apt-get install screen``` to detached the running terminals from SSH.

- Run Django
    - ```su```
    - ```root```
    - ```cd /home/ubuntu/django_project/```
    - ```source my-django/bin/activate```
    - ```cd /home/ubuntu/django_project/mysite/```
    - ```python manage.py runserver 0.0.0.0:80 --insecure```
- Run auto update script
    - cd to the directory of "Utility Scripts"
    - ```python Auto_update.py```
