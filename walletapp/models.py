from django.db import models
from django.contrib.auth.models import User
from payapp.models import Currency


# Create your models here.
class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(default=1000, decimal_places=2, max_digits=15)
    currency = models.CharField(max_length=5, choices=Currency.choices, default=Currency.GBP)

    def __str__(self) -> str:
        return self.user.username
