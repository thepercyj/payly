from django.contrib.auth.decorators import user_passes_test

def is_superuser(user):
    return user.is_superuser or False

def admin_required(fn=None,**args):
    decorator=user_passes_test(is_superuser,**args)
    if fn:
        return decorator(fn)
    return decorator