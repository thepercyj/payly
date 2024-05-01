from django.contrib.auth.models import User
from payapp.models import Transaction
from django.db.models import Q


def get_no_of_users():
    """
    Returns the number of users in the system.

    :return: int: Number of users in the system.
    """
    return User.objects.count()


def get_no_of_transactions(success=True):
    """
    Returns the number of transactions in the system.

    :param success: bool, optional
        Indicates whether to count successful transactions (default is True).
    :type success: bool
    :return: QuerySet
        QuerySet containing the transactions filtered by status.
    """

    arg = 'SUCCESS' if success else 'PENDING'
    return Transaction.objects.filter(
        Q(status__exact=arg)
    ).all()


def get_all_transactions():
    """
    Returns all transactions in the system.

    :return: QuerySet
        QuerySet containing all transactions.
    """
    return Transaction.objects.all()


def get_all_users(current_user: User):
    """
    Returns all users in the system except the current user.

    :param current_user: User
        The current user whose ID will be excluded from the query.
    :type current_user: User
    :return: QuerySet
        QuerySet containing all users except the current user.
    """
    return User.objects.exclude(id=current_user.id)
