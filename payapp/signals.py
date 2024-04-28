from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from register.forms import save_profile_picture
from .models import UserProfile


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create UserProfile for the newly created user
        user_profile = UserProfile.objects.create(user=instance)
        print('UserProfile created.')

        # Select a random profile picture and save it to the user profile
        profile_picture = save_profile_picture()
        user_profile.profile_picture = profile_picture
        user_profile.save()
        print('Random profile picture assigned.')
    else:
        # If the user already exists, simply save the UserProfile
        instance.userprofile.save()
        print('UserProfile updated.')