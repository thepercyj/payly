from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Currency(models.TextChoices):
    GBP = 'GBP', 'British Pound'
    USD = 'USD', 'United States Dollar'
    EUR = 'EUR', 'Euro'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    main_currency = models.CharField(max_length=5, choices=Currency.choices, default=Currency.GBP)
    profile_picture = models.ImageField(upload_to='profile', blank=True, default='default.png')

    def __str__(self) -> str:
        return f'Profile [ {self.user.username} ]'
