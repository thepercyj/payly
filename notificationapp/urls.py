from django.urls import path
from . import views

urlpatterns = [
    path('notification/', views.notification, name='notification'),
    path('notification-seen/', views.notification_seen, name='notification-seen'),
]

htmxpatterns = [
    path('modal/get-notification', views.get_notifications, name='get-notifications')
]
urlpatterns += htmxpatterns
