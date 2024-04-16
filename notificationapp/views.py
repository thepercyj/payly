from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .core.notifications import get_user_notifications


@login_required(login_url='login')
def notification(request):
    notifications = get_user_notifications(request.user.id, limit=10)
    context = {
        'notifications': notifications.all(),
        'count': len(notifications)
    }
    return render(request, 'notificationapp/layout/notification-detail.html', context)


@login_required(login_url='login')
def get_notifications(request):
    notifications = get_user_notifications(request.user.id, limit=5)
    context = {
        'notifications': notifications.all(),
        'count': len(notifications)
    }
    return render(request, 'notificationapp/layout/notification-list.html', context)
