from django.shortcuts import redirect


def redirect_if_not_super_user(request):
    if not request.user.is_superuser:
        return redirect('login')
    return True
