from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import models
from notificationapp.models import Notification


@receiver(post_save, sender=Notification)
def update_notification_count_on_save(sender, instance, created, **kwargs):
    if instance.seen:
        Notification.objects.filter(user=instance.user, seen=False).update(
            notification_count=models.F('notification_count') - 1)
    else:
        Notification.objects.filter(user=instance.user, seen=False).update(
            notification_count=models.F('notification_count') + 1)


@receiver(post_delete, sender=Notification)
def update_notification_count_on_delete(sender, instance, **kwargs):
    if not instance.seen:
        Notification.objects.filter(user=instance.user, seen=False).update(
            notification_count=models.F('notification_count') + 1)
