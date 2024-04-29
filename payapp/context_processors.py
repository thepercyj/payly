from payapp.models import UserProfile

def get_profile_picture(request):
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        return {'user_profile': user_profile}
    else:
        return {'user_profile': None}