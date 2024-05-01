from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from register.forms import save_profile_picture
from .models import UserProfile


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Signal receiver function to create or update a user profile when a User instance is saved.

    :param sender: class
        The class from which the signal is sent.
    :param instance: User
        The instance of the User model that was saved.
    :param created: bool
        Indicates whether the User instance was created or updated.
    :param kwargs: dict
        Additional keyword arguments passed to the signal.
    """
    if created:
        user_profile = UserProfile.objects.create(user=instance)

        profile_picture = save_profile_picture()
        user_profile.profile_picture = profile_picture
        user_profile.save()
    else:
        instance.userprofile.save()