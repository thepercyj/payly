from django.contrib.auth.models import User
from django.db.models import Q


def search_by_identifier(identifier):
    """
    Searches for users based on a given identifier.

    :param identifier: str
        The identifier to search for, which can be an email, first name, last name, or username.
    :return: list
        A list of User objects matching the search criteria.
    """
    result = User.objects.filter(
        Q(email__startswith=identifier) |
        Q(first_name__startswith=identifier) |
        Q(last_name__startswith=identifier) |
        Q(username__startswith=identifier)
    )
    return list(result.all())


def search_by_username(username):
    """
    Searches for a user by username.

    :param username: str
        The username of the user to search for.
    :return: User
        The User object matching the given username.
    """

    result = User.objects.get(username=username)
    return result


def search_by_id(id):
    """
    Searches for a user by ID.

    :param id: int
        The ID of the user to search for.
    :return: User
        The User object matching the given ID.
    """
    result = User.objects.get(id=id)
    return result
