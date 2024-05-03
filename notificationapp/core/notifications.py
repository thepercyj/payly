import uuid
import thriftpy2
from thriftpy2.rpc import make_client
from thriftpy2.thrift import TException
from datetime import datetime
from django.http import HttpResponse
from ..models import NotificationType, Notification
from django.contrib.auth.models import User
from django.db.models import Q


timestamp_thrift = thriftpy2.load(
    'timestamp.thrift', module_name='timestamp_thrift')
Timestamp = timestamp_thrift.TimestampService


def notify(userid: int, title: str, message: str, type: NotificationType = NotificationType.INFO):
    """
    Notify the user with a new notification.

    Args:
        userid (int): The ID of the user to notify.
        title (str): The title of the notification.
        message (str): The message content of the notification.
        type (NotificationType, optional): The type of the notification. Defaults to NotificationType.INFO.

    Returns:
        bool or HttpResponse: True if the notification is successfully created, otherwise an HttpResponse with an error message.
    """
    try:
        client = make_client(Timestamp, '127.0.0.1', 10000)
        timestamp = datetime.fromtimestamp(int(str(client.getCurrentTimestamp())))
        notification = Notification(nid=uuid.uuid4(), user=User.objects.get(id=userid), type=type, message=message,
                                title=title, datetime=timestamp)
        notification.save()
    except TException as e:
        return HttpResponse("An error occurred: {}".format(str(e)))

    return True


def get_user_notifications(userid: int, limit=100):
    """
    Retrieve notifications for a specific user.

    Args:
        userid (int): The ID of the user whose notifications are to be retrieved.
        limit (int, optional): The maximum number of notifications to retrieve. Defaults to 100.

    Returns:
        QuerySet: A QuerySet containing the user's notifications.
    """
    limit = limit or 100
    notifications = Notification.objects.filter(
        Q(user_id__exact=userid)
    ).order_by('-datetime')[:limit]

    return notifications.all()
