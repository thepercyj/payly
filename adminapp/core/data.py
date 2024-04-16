from django.contrib.auth.models import User
from payapp.models import Transaction
from django.db.models import Q


def get_no_of_users():
    return User.objects.count()


def get_no_of_transactions(success=True):
    arg = 'SUCCESS' if success else 'PENDING'
    return Transaction.objects.filter(
        Q(status__exact=arg)
    ).all()


def get_all_transactions():
    return Transaction.objects.all()


def get_all_users(current_user: User):
    return User.objects.exclude(id=current_user.id)
