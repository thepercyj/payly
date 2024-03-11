from django.urls import path
from . import views

urlpatterns = [
    path('payapp/', views.dashboard, name='dashboard'),
    path('payapp/transaction/', views.transaction, name='transaction'),
    path('payapp/send/', views.send_money, name='send_money'),
    path('payapp/request/', views.request_money, name='request_money'),
    path('payapp/help/', views.help, name='help'),
    path('logout/',views.logout,name='logout')

]
