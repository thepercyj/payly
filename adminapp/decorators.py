from django.contrib.auth.decorators import user_passes_test


def is_superuser(user):
    """
    Checks if a user is a superuser.

    :param user: User
        The user object to check for superuser status.
    :type user: User
    :return: bool
        Returns True if the user is a superuser, otherwise returns False.
    """
    return user.is_superuser or False


def admin_required(fn=None, **args):
    """
    Decorator to restrict access to views to only superusers.

    :param fn: function, optional
        The function to be decorated. If not provided, returns a decorator.
    :type fn: function
    :param args: additional arguments for user_passes_test decorator.
    :type args: dict
    :return: function or decorator
        If fn is provided, returns the decorated function. Otherwise, returns the decorator.
    """
    decorator = user_passes_test(is_superuser, **args)
    if fn:
        return decorator(fn)
    return decorator
