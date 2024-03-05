from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout


# Create your views here.
@login_required(login_url='login')
def index(request):
    if request.user.is_superuser:
        return redirect('admin')
    return render(request,'payapp/dashboard.html',{'title':'Dashboard'})


def logout(request):
    auth_logout(request)
    return redirect('login')
