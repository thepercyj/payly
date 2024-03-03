from django.urls import path
from . import views

urlpatterns = [
    path('', views.register_user, name='register'),
    path('login/', views.login, name='login'),

]
