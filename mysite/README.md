# EECS E6895 - A-share Stock Auto Trader
B9: Investment Strategy - AI Trader (CN/HK/TW/JP)

## Team
Yiwen Fang (yf2560) | Guoshiwen Han (gh2567)

## Note
- Python env: conda activate my-django
- python=3.8.8
- pip install Django==3.1.7
- pip install yahoo-fin
- pip install django-bootstrap4
- pip install matplotlib
- pip install grpcio==1.27.2
- pip install tensorflow --no-cache-dir
- pip install numpy
- pip install pandas
- pip install scikit-learn
- pip install statsmodels

## Command
```
python manage.py runserver
pip install -r requirements.txt
```

## Run .py locally, not from HTTP
```
conda activate my-django
python Auto_update.py
python Batch_train.py
```

## Run in AWS EC2
```
su
root
cd /home/ubuntu/django_project/
source my-django/bin/activate
cd /home/ubuntu/django_project/mysite/
python manage.py runserver 0.0.0.0:80
```

```
apt-get install screen
```
