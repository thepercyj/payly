from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import models
from notificationapp.models import Notification


@receiver(post_save, sender=Notification)
def update_notification_count_on_save(sender, instance, created, **kwargs):
    """
    Updates the notification count when a notification is saved.

    :param sender: Model
        The sender model of the signal.
    :param instance: Notification
        The instance of the Notification model being saved.
    :param created: bool
        Indicates whether the instance was created or updated.
    :param kwargs: dict
        Additional keyword arguments.
    :return: None
    """

    if instance.seen:
        Notification.objects.filter(user=instance.user, seen=False).update(
            notification_count=models.F('notification_count') - 1)
    else:
        Notification.objects.filter(user=instance.user, seen=False).update(
            notification_count=models.F('notification_count') + 1)


@receiver(post_delete, sender=Notification)
def update_notification_count_on_delete(sender, instance, **kwargs):
    """
    Updates the notification count when a notification is deleted.

    :param sender: Model
        The sender model of the signal.
    :param instance: Notification
        The instance of the Notification model being deleted.
    :param kwargs: dict
        Additional keyword arguments.
    :return: None
    """

    if not instance.seen:
        Notification.objects.filter(user=instance.user, seen=False).update(
            notification_count=models.F('notification_count') + 1)
