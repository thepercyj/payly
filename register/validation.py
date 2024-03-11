from django.contrib.auth.models import User
from django.db.models import Q


def user_email_exists(email):
    return len(User.objects.filter(email=email)) > 0


def username_exists(username):
    return len(User.objects.filter(username=username)) > 0


def identifier_search(identifier):
    results = User.objects.filter(
        Q(email__contains=identifier) |
        Q(username__contains=identifier) |
        Q(first_name__contains=identifier) |
        Q(last_name__contains=identifier))
    return results
