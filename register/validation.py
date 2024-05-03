from django.contrib.auth.models import User
from django.db.models import Q


def user_email_exists(email):
    """
    Checks if a user with the given email exists in the database.

    :param email: The email to check.
    :return: True if a user with the email exists, False otherwise.
    """

    return len(User.objects.filter(email=email)) > 0


def username_exists(username):
    """
    Checks if a user with the given username exists in the database.

    :param username: The username to check.
    :return: True if a user with the username exists, False otherwise.
    """
    return len(User.objects.filter(username=username)) > 0


def identifier_search(identifier):
    """
    Searches for users based on the given identifier.

    :param identifier: The search identifier.
    :return: Queryset of users matching the search.
    """
    results = User.objects.filter(
        Q(email__contains=identifier) |
        Q(username__contains=identifier) |
        Q(first_name__contains=identifier) |
        Q(last_name__contains=identifier))
    return results
