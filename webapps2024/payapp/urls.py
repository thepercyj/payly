from django.urls import path
from . import views

urlpatterns = [
    path('payapp/', views.dashboard, name='dashboard'),
    path('payapp/transaction/', views.transaction, name='transaction'),
    path('payapp/dash-send/', views.dash_send, name='dash_send'),
    path('payapp/dash-request/', views.dash_request, name='dash_request'),
    path('logout/',views.logout,name='logout')

]
