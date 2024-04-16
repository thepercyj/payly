from payapp.models import UserProfile


def profile_id(userid):
    profile = UserProfile.objects.get(user_id=userid)
    return profile
