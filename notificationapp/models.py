from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class NotificationType(models.TextChoices):
    """
    Defines choices for different types of notifications.

    Choices:
        MONEY_REQUEST: Money Request
        MONEY_RECIEVED: Money Received
        TRANSACTION_SUCCESS: Transaction Success
        TRANSACTION_PENDING: Transaction Pending
        TRANSACTION_DECLINED: Transaction Declined
        ACCOUNT_VERIFIED: Account Verified
        ACCOUNT_SUSPENDED: Account Suspended
        INFO: Information
    """

    MONEY_REQUEST = 'MONREQ', 'Money Request'
    MONEY_RECIEVED = 'MONREC', 'Money Recieved'
    TRANSACTION_SUCCESS = 'TRANSUC', 'Transaction Success'
    TRANSACTION_PENDING = 'TRANPEN', 'Transaction Pending'
    TRANSACTION_DECLINED = 'TRANDEC', 'Transaction Declined'
    ACCOUNT_VERIFIED = 'ACCVER', 'Account Verified'
    ACCOUNT_SUSPENDED = 'ACCSUS', 'Account Suspended'
    INFO = 'INFO', 'Information'


class Notification(models.Model):
    """
    Represents a notification for a user.

    Attributes:
        nid (str): Notification ID.
        user (ForeignKey): The user associated with the notification.
        type (str): The type of notification.
        datetime (DateTimeField): The datetime when the notification was created.
        seen (bool): Indicates whether the notification has been seen by the user.
        message (str): The message content of the notification.
        title (str): The title of the notification.
        notification_count (int): The count of notifications for the user.

    Methods:
        mark_as_read(): Marks the notification as read.
    """

    nid = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification_user')
    type = models.CharField(max_length=10, choices=NotificationType.choices, default=NotificationType.INFO)
    datetime = models.DateTimeField(auto_now_add=False)
    seen = models.BooleanField(default=False)
    message = models.TextField(default="")
    title = models.TextField(default="")
    notification_count = models.IntegerField(default=0)

    def mark_as_read(self):
        """
        Marks the notification as read.

        :return: None
        """

        self.seen = True
        self.save()
        return None
