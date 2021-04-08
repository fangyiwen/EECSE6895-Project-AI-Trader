from django.urls import path

from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('', views.index, name='index'),
                  path('select_stock/', views.select_stock,
                       name='select_stock'),
                  path('trade_stock_lstm/<str:stock_id>/',
                       views.trade_stock_lstm, name='trade_stock_lstm'),
                  path('trade_run_lstm/<str:stock_id>/<str:initial_balance>/',
                       views.trade_run_lstm, name='trade_run_lstm'),
                  path('trade_stock_svm/<str:stock_id>/',
                       views.trade_stock_svm, name='trade_stock_svm'),
                  path('trade_run_svm/<str:stock_id>/',
                       views.trade_run_svm, name='trade_run_svm'),
                  path('train_lstm/<str:stock_id>/',
                       views.train_lstm, name='train_lstm')
              ] + static(settings.STATIC_URL,
                         document_root=settings.STATIC_ROOT)
