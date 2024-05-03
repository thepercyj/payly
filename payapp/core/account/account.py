from payapp.models import UserProfile


def profile_id(userid):
    """
    Retrieves the user profile associated with the given user ID.

    :param userid: int
        The ID of the user whose profile is to be retrieved.
    :type userid: int
    :return: UserProfile
        The user profile associated with the given user ID.
    """
    profile = UserProfile.objects.get(user_id=userid)
    return profile
