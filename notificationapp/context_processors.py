from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from notificationapp.models import Notification


def get_notifications(request):
    notification_count = None
    if request.user.is_authenticated:
        user = request.user
        notification_count = Notification.objects.filter(user=user, seen=False).count()
        return {'notification_count': notification_count}
    else:
        return{'notification_count': notification_count}
