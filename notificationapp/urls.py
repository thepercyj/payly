from django.urls import path
from . import views

urlpatterns = [
path('notification/', views.notification, name='notification'),
]

htmxpatterns = [
    path('htmx/get-notification', views.get_notifications, name='get-notifications')
]
urlpatterns += htmxpatterns
