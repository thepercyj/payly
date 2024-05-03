from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Currency(models.TextChoices):
    """
    Enumeration representing currency choices.

    :cvar GBP: str
        British Pound
    :cvar USD: str
        United States Dollar
    :cvar EUR: str
        Euro
    """
    GBP = 'GBP', 'British Pound'
    USD = 'USD', 'United States Dollar'
    EUR = 'EUR', 'Euro'


class UserProfile(models.Model):
    """
    Model representing a user profile.

    :ivar user: User
        The associated user.
    :ivar profile_picture: ImageField
        The profile picture of the user.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile', blank=True, default='profile.jpg')

    def __str__(self) -> str:
        """
        Returns the string representation of the user profile.

        :return: str
            The string representation of the user profile.
        """
        return f'Profile [ {self.user.username} ]'


class TransactionStatus(models.TextChoices):
    """
    Enumeration representing transaction status choices.

    :cvar SUCCESS: str
        Success
    :cvar DECLINED: str
        Declined
    :cvar PENDING: str
        Pending
    """

    SUCCESS = 'SUCCESS', 'Success'
    DECLINED = 'DECLINED', 'Declined'
    PENDING = 'PENDING', 'Pending'


class OperationType(models.TextChoices):
    """
    Enumeration representing operation type choices.

    :cvar DEBIT: str
        Debit
    :cvar CREDIT: str
        Credit
    """
    DEBIT = 'DEBIT', 'Debit'
    CREDIT = 'CREDIT', 'Credit'


class Transaction(models.Model):
    """
    Model representing a transaction.

    :ivar tid: str
        The transaction ID.
    :ivar sender: User
        The sender of the transaction.
    :ivar receiver: User
        The receiver of the transaction.
    :ivar amount: Decimal
        The amount of the transaction.
    :ivar balance: Decimal
        The balance after the transaction.
    :ivar currency: str
        The currency of the transaction.
    :ivar status: str
        The status of the transaction.
    :ivar datetime: datetime
        The datetime of the transaction.
    """

    tid = models.CharField(max_length=255)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    balance = models.DecimalField(decimal_places=2, max_digits=12)
    currency = models.CharField(max_length=5, choices=Currency.choices, default=Currency.GBP)
    status = models.CharField(max_length=10, choices=TransactionStatus.choices, default=TransactionStatus.PENDING)
    datetime = models.DateTimeField(auto_now_add=False)

    def type(self, source_user: User):
        """
        Determines the type of the transaction.

        :param source_user: User
            The user to determine the type for.
        :return: str
            The type of the transaction.
        """
        if source_user.id == self.id:
            return 'DEBIT'
        return 'CREDIT'


class TransferStatus(models.TextChoices):
    """
    Enumeration representing transfer status choices.

    :cvar APPROVED: str
        Approved
    :cvar DENIED: str
        Denied
    :cvar PENDING: str
        Pending
    """
    APPROVED = 'APPROVED', 'Approved'
    DENIED = 'DENIED', 'Denied'
    PENDING = 'PENDING', 'Pending'


class TransferRequest(models.Model):
    """
    Model representing a transfer request.

    :ivar rid: str
        The request ID.
    :ivar sender: User
        The sender of the request.
    :ivar receiver: User
        The receiver of the request.
    :ivar source: User
        The source of the request.
    :ivar amount: Decimal
        The amount of the request.
    :ivar currency: str
        The currency of the request.
    :ivar status: str
        The status of the request.
    :ivar datetime: datetime
        The datetime of the request.
    """

    rid = models.CharField(max_length=255)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='request_sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='request_receiver')
    source = models.ForeignKey(User, on_delete=models.CASCADE, related_name='request_source', default=None)
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    currency = models.CharField(max_length=5, choices=Currency.choices, default=Currency.GBP)
    status = models.CharField(max_length=10, choices=TransferStatus.choices, default=TransferStatus.PENDING)
    datetime = models.DateTimeField(auto_now_add=False)


class BankAccount(models.Model):
    """
    Model representing a bank account.

    :ivar bank: str
        The name of the bank.
    :ivar owner: User
        The owner of the bank account.
    :ivar account_no: str
        The account number.
    """
    bank = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='account_owner')
    account_no = models.CharField(max_length=255)
