from notificationapp.models import Notification


def get_notifications(request):
    """
    Retrieves the count of unread notifications for the authenticated user.

    :param request: HttpRequest
        The request object containing information about the current HTTP request.
    :type request: HttpRequest
    :return: dict
        A dictionary containing the count of unread notifications.
    """
    notification_count = None
    if request.user.is_authenticated:
        user = request.user
        notification_count = Notification.objects.filter(user=user, seen=False).count()
        return {'notification_count': notification_count}
    else:
        return{'notification_count': notification_count}
