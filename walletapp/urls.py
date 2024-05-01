from django.urls import path
from . import views

urlpatterns = [
    path('', views.wallet, name='wallet')
]

htmxpatterns = [
    path('modal/add-money', views.get_add_money, name='add-money'),
    path('modal/change-currency', views.get_change_currency, name='change-currency'),
    path('modal/balance', views.get_balance, name='balance'),
    path('modal/currency', views.get_currency, name='currency')
]

urlpatterns += htmxpatterns
