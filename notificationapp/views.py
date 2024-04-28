from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .core.notifications import get_user_notifications
from .models import Notification


@login_required(login_url='login')
def notification(request):
    user = request.user
    notification_count = Notification.objects.filter(user=user, seen=False).count()
    notifications = get_user_notifications(user.id, limit=10)
    context = {
        'notifications': notifications.all(),
        'notification_count': notification_count
    }
    return render(request, 'notificationapp/layout/notification-detail.html', context)


@login_required(login_url='login')
def get_notifications(request):
    user = request.user
    notification_count = Notification.objects.filter(user=user, seen=False).count()
    notifications = get_user_notifications(user.id, limit=5)
    context = {
        'notifications': notifications.all(),
        'notification_count': notification_count
    }
    return render(request, 'notificationapp/layout/notification-list.html', context)
