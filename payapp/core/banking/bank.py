from payapp.models import BankAccount as BA
from django.contrib.auth.models import User as U


def add_bank_acc(bank: str, account_no: str, user: U) -> BA:
    """
    Adds a new bank account for the user.

    :param bank: str
        The name of the bank.
    :param account_no: str
        The account number.
    :param user: U
        The user who owns the bank account.
    :return: BA
        The newly created bank account.
    """
    new_account = BA(bank=bank, account_no=account_no, owner=user)
    new_account.save()
    return new_account


def delete_bank_acc(account_id: int):
    """
    Deletes an existing bank account from the database.

    :param account_id: int
        The ID of the bank account to be deleted.
    :return: bool
        Returns True if the bank account is successfully deleted.
    """

    account = BA.objects.get(id=account_id)
    account.delete()
    return True


def update_bank_acc(account_id: int, bank: str, account_no: str, user: U) -> BA:
    """
    Updates an existing bank account.

    :param account_id: int
        The ID of the bank account to be updated.
    :param bank: str
        The new name of the bank.
    :param account_no: str
        The new account number.
    :param user: U
        The user who owns the bank account.
    :return: BA
        The updated bank account.
    """

    account = BA.objects.get(id=account_id)
    account.bank = bank
    account.account_no = account_no
    account.owner = user
    account.save()
    return account


def get_user_bank_acc(user_id: int):
    """
    Retrieves a list of bank accounts for the user.

    :param user_id: int
        The ID of the user.
    :return: QuerySet
        A queryset containing the bank accounts of the user.
    """

    return BA.objects.filter(owner_id__exact=user_id).all()


def get_acc_id(id: int):
    """
    Retrieves bank account details by ID.

    :param id: int
        The ID of the bank account.
    :return: BA
        The bank account object.
    """
    return BA.objects.get(id=id)
