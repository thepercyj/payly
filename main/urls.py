from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout')
]

htmxpatterns = [
    path('modal/alert', views.alert, name='alert'),
    path('modal/recent-transfers/', views.recent_transfers, name='recent-transfers'),
]

urlpatterns += htmxpatterns
