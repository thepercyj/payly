from django.urls import path
from . import views

urlpatterns = [
    path('<str:currency1>/<str:currency2>/<int:amount>', views.currency_conversion, name='currency_conversion')
]
