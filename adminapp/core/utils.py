from django.shortcuts import redirect


def redirect_if_not_super_user(request):
    """
    Redirects the user to the login page if they are not a superuser.

    :param request: HttpRequest
        The request object containing information about the current HTTP request.
    :type request: HttpRequest
    :return: bool or HttpResponseRedirect
        Returns True if the user is a superuser, otherwise redirects to the login page.
    """
    if not request.user.is_superuser:
        return redirect('login')
    return True
