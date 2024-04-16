from django.urls import path
from . import views

urlpatterns = [
    path('', views.wallet, name='wallet')
]

htmxpatterns = [
    path('htmx/add-money', views.get_add_money, name='add-money'),
    path('htmx/change-currency', views.get_change_currency, name='change-currency'),
    path('htmx/balance', views.get_balance, name='balance'),
    path('htmx/currency', views.get_currency, name='currency')
]

urlpatterns += htmxpatterns
