from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import logout as logout_view


# Create your views here.
@login_required(login_url='login')
def dashboard(request):
    if request.user.is_superuser:
        return redirect('admin')
    return render(request, 'payapp/dashboard.html', {'title': 'Dashboard'})


def logout(request):
    logout_view(request)
    return redirect('login')


@login_required(login_url='login')
def transaction(request):
    return render(request, 'payapp/transaction.html')


@login_required(login_url='login')
def send_money(request):
    return render(request, 'payapp/send.html')


@login_required(login_url='login')
def request_money(request):
    return render(request, 'payapp/request.html')


@login_required(login_url='login')
def help(request):
    return render(request, 'payapp/help.html')