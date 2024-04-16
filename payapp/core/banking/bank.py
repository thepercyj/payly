from payapp.models import BankAccount as BA
from django.contrib.auth.models import User as U


# Create a new bank account for a user
def add_bank_acc(bank: str, account_no: str, user: U) -> BA:
    new_account = BA(bank_name=bank, acc_no=account_no, owner=user)
    new_account.save()
    return new_account


# Remove an existing bank account from the database
def delete_bank_acc(account_id: int):
    account = BA.objects.get(id=account_id)
    account.delete()
    return True


# Update an existing bank account
def update_bank_acc(account_id: int, bank: str, account_no: str, user: U) -> BA:
    account = BA.objects.get(id=account_id)
    account.bank_name = bank
    account.acc_no = account_no
    account.owner = user
    account.save()
    return account


# Get a list of bank accounts for a user
def get_user_bank_acc(user_id: int):
    return BA.objects.filter(owner_id__exact=user_id).all()


# Get bank account details with ID
def get_acc_id(account_id: int):
    return BA.objects.get(id=account_id)
