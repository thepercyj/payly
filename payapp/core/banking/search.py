from django.contrib.auth.models import User
from django.db.models import Q


def search_by_identifier(identifier):
    result = User.objects.filter(
        Q(email__startswith=identifier) |
        Q(first_name__startswith=identifier) |
        Q(last_name__startswith=identifier) |
        Q(username__startswith=identifier)
    )
    return list(result.all())


def search_by_username(username):
    result = User.objects.get(username=username)
    return result


def search_by_id(id):
    result = User.objects.get(id=id)
    return result
