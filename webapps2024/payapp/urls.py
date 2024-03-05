from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='dashboard'),
    path('logout/', views.logout, name='logout')
]
