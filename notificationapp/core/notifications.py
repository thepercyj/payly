from datetime import datetime

from django.http import HttpResponse

from ..models import NotificationType, Notification
from django.contrib.auth.models import User
from django.db.models import Q
import uuid
import thriftpy
from thriftpy.rpc import make_client
from thriftpy.thrift import TException


timestamp_thrift = thriftpy.load(
    'timestamp.thrift', module_name='timestamp_thrift')
Timestamp = timestamp_thrift.TimestampService


def notify(userid: int, title: str, message: str, type: NotificationType = NotificationType.INFO):

    try:
        client = make_client(Timestamp, '127.0.0.1', 9090)
        timestamp = datetime.fromtimestamp(int(str(client.getCurrentTimestamp())))
        notification = Notification(nid=uuid.uuid4(), user=User.objects.get(id=userid), type=type, message=message,
                                title=title, datetime=timestamp)
        notification.save()
    except TException as e:
        return HttpResponse("An error occurred: {}".format(str(e)))

    return True


def get_user_notifications(userid: int, limit=100):
    limit = limit or 100
    notifications = Notification.objects.filter(
        Q(user_id__exact=userid)
    ).order_by('-datetime')[:limit]

    return notifications.all()
