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


class TransactionStatus(models.TextChoices):
    SUCCESS = 'SUCCESS', 'Success'
    DECLINED = 'DECLINED', 'Declined'
    PENDING = 'PENDING', 'Pending'


class OperationType(models.TextChoices):
    DEBIT = 'DEBIT', 'Debit'
    CREDIT = 'CREDIT', 'Credit'


# Create your models here.
class Transaction(models.Model):
    tid = models.CharField(max_length=255)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    balance = models.DecimalField(decimal_places=2, max_digits=12)
    currency = models.CharField(max_length=5, choices=Currency.choices, default=Currency.GBP)
    status = models.CharField(max_length=10, choices=TransactionStatus.choices, default=TransactionStatus.PENDING)
    datetime = models.DateTimeField(auto_now_add=True)

    def type(self, source_user: User):
        if source_user.id == self.id:
            return 'DEBIT'
        return 'CREDIT'


class TransferStatus(models.TextChoices):
    APPROVED = 'APPROVED', 'Approved'
    DENIED = 'DENIED', 'Denied'
    PENDING = 'PENDING', 'Pending'


# Create your models here.
class TransferRequest(models.Model):
    rid = models.CharField(max_length=255)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='request_sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='request_receiver')
    source = models.ForeignKey(User, on_delete=models.CASCADE, related_name='request_source', default=None)
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    currency = models.CharField(max_length=5, choices=Currency.choices, default=Currency.GBP)
    status = models.CharField(max_length=10, choices=TransferStatus.choices, default=TransferStatus.PENDING)
    datetime = models.DateTimeField(auto_now_add=True)


class BankAccount(models.Model):
    bank = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='account_owner')
    account_no = models.CharField(max_length=255)
