from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from .core.notifications import get_user_notifications


@login_required(login_url='login')
def notification(request):
    """
    Renders the page displaying detailed notifications for the authenticated user.

    :param request: HttpRequest
        The request object containing information about the current HTTP request.
    :type request: HttpRequest
    :return: HttpResponse
        The rendered page displaying detailed notifications.
    """

    user = request.user
    notifications = get_user_notifications(user.id, limit=10)
    context = {
        'notifications': notifications.all(),
    }
    return render(request, 'notificationapp/layout/notification-detail.html', context)


@login_required(login_url='login')
def get_notifications(request):
    """
    Renders the page displaying a list of notifications for the authenticated user.

    :param request: HttpRequest
        The request object containing information about the current HTTP request.
    :type request: HttpRequest
    :return: HttpResponse
        The rendered page displaying a list of notifications.
    """

    user = request.user
    notifications = get_user_notifications(user.id, limit=3)
    context = {
        'notifications': notifications.all(),
    }
    return render(request, 'notificationapp/layout/notification-list.html', context)


@login_required(login_url='login')
def notification_seen(request):
    """
    Marks all notifications as seen for the authenticated user.

    :param request: HttpRequest
        The request object containing information about the current HTTP request.
    :type request: HttpRequest
    :return: JsonResponse
        A JSON response indicating that the notifications have been marked as seen.
    """

    user = request.user
    notifications = get_user_notifications(user.id, limit=5)
    for notification in notifications:
            notification.mark_as_read()

    return JsonResponse({'message': 'Notifications marked as seen'}, status=200)
