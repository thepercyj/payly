from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class NotificationType(models.TextChoices):
    MONEY_REQUEST = 'MONREQ', 'Money Request'
    MONEY_RECIEVED = 'MONREC', 'Money Recieved'
    TRANSACTION_SUCCESS = 'TRANSUC', 'Transaction Success'
    TRANSACTION_PENDING = 'TRANPEN', 'Transaction Pending'
    TRANSACTION_DECLINED = 'TRANDEC', 'Transaction Declined'
    ACCOUNT_VERIFIED = 'ACCVER', 'Account Verified'
    ACCOUNT_SUSPENDED = 'ACCSUS', 'Account Suspended'
    INFO = 'INFO', 'Information'


class Notification(models.Model):
    nid = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification_user')
    type = models.CharField(max_length=10, choices=NotificationType.choices, default=NotificationType.INFO)
    datetime = models.DateTimeField(auto_now_add=False)
    seen = models.BooleanField(default=False)
    # data=models.TextField(default='None')
    message = models.TextField(default="")
    title = models.TextField(default="")
