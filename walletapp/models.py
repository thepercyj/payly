from django.db import models
from django.contrib.auth.models import User
from payapp.models import Currency


class Wallet(models.Model):
    """
    Model representing a user's wallet.

    Attributes:
        user (User): The user associated with the wallet.
        balance (Decimal): The balance in the wallet.
        currency (str): The currency of the wallet.

    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(default=1000, decimal_places=2, max_digits=15)
    currency = models.CharField(max_length=5, choices=Currency.choices, default=Currency.GBP)

    def __str__(self) -> str:
        """
        Returns a string representation of the wallet.

        :return: The username of the user associated with the wallet.
        """
        return self.user.username
