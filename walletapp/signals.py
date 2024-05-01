from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Wallet


@receiver(post_save, sender=User)
def create_wallet(sender, instance, created, **kwargs):
    """
    Signal receiver function to create a wallet for a newly created user.

    Args:
        sender: The sender of the signal.
        instance (User): The instance of the user being saved.
        created (bool): Indicates whether the user instance is newly created.
        **kwargs: Additional keyword arguments.

    """
    if created:
        Wallet.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_wallet(sender, instance, **kwargs):
    """
    Signal receiver function to save the wallet of a user.

    Args:
        sender: The sender of the signal.
        instance (User): The instance of the user being saved.
        **kwargs: Additional keyword arguments.

    """
    instance.wallet.save()