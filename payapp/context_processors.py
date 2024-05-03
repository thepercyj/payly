from payapp.models import UserProfile


def get_profile_picture(request):
    """
    Retrieves the profile picture of the authenticated user.

    :param request: HttpRequest
        The request object containing information about the current HTTP request.
    :return: dict
        A dictionary containing the user profile picture, or None if the user is not authenticated.
    """
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        return {'user_profile': user_profile}
    else:
        return {'user_profile': None}
