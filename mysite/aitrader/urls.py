from django.urls import path

from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('', views.index, name='index'),
                  path('select_stock/', views.select_stock,
                       name='select_stock'),
                  path('train_stock/', views.train_stock,
                       name='train_stock'),
                  path('trade_stock_lstm/<str:stock_id>/',
                       views.trade_stock_lstm, name='trade_stock_lstm'),
                  path('trade_stock_svm/<str:stock_id>/',
                       views.trade_stock_svm, name='trade_stock_svm'),
                  path('trade_stock_arima/<str:stock_id>/',
                       views.trade_stock_arima, name='trade_stock_arima'),
                  path('trade_stock_integration/<str:stock_id>/',
                       views.trade_stock_integration,
                       name='trade_stock_integration'),
                  path('trade_run_lstm/<str:stock_id>/<str:initial_balance>/',
                       views.trade_run_lstm, name='trade_run_lstm'),
                  path('trade_run_svm/<str:stock_id>/',
                       views.trade_run_svm, name='trade_run_svm'),
                  path('trade_run_arima/<str:stock_id>/<str:initial_balance>/',
                       views.trade_run_arima, name='trade_run_arima'),
                  path('trade_run_integration/<str:stock_id>/',
                       views.trade_run_integration,
                       name='trade_run_integration'),
                  path('train_lstm/<str:stock_id>/',
                       views.train_lstm, name='train_lstm'),
                  path('train_svm/<str:stock_id>/',
                       views.train_svm, name='train_svm'),
                  path('train_arima/<str:stock_id>/',
                       views.train_arima, name='train_arima')
              ] + static(settings.STATIC_URL,
                         document_root=settings.STATIC_ROOT)
