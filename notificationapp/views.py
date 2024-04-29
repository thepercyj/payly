from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from payapp.models import UserProfile
from .core.notifications import get_user_notifications
from .models import Notification


@login_required(login_url='login')
def notification(request):
    user = request.user
    notifications = get_user_notifications(user.id, limit=10)
    context = {
        'notifications': notifications.all(),
    }
    return render(request, 'notificationapp/layout/notification-detail.html', context)


@login_required(login_url='login')
def get_notifications(request):
    user = request.user
    notifications = get_user_notifications(user.id, limit=3)
    context = {
        'notifications': notifications.all(),
    }
    return render(request, 'notificationapp/layout/notification-list.html', context)


@login_required(login_url='login')
def notification_seen(request):
    user = request.user
    notifications = get_user_notifications(user.id, limit=5)
    for notification in notifications:
            notification.mark_as_read()

    return JsonResponse({'message': 'Notifications marked as seen'}, status=200)
