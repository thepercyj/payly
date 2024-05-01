from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout')
]

htmxpatterns = [
    path('htmx/alert', views.alert, name='alert'),
    path('htmx/recent-transfers/', views.recent_transfers, name='recent-transfers'),
]

urlpatterns += htmxpatterns
