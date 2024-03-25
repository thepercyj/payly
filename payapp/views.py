from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout as logout_view

from popup.toast import ToastHttpResponse
from .forms import EditUserProfileForm


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
def profile(request):
    return render(request, 'payapp/profile.html')


@login_required(login_url='login')
def edit_profile(request):
    form = EditUserProfileForm(request.user)

    if request.method == 'POST':
        form = EditUserProfileForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            print('Your profile has been successfully updated.')
            return redirect('profile')

    context = {
        'editform': form,
        'user': request.user
    }
    return render(request, 'payapp/modal/edit-profile.html', context)


@login_required(login_url='login')
def send_money(request):
    return render(request, 'payapp/send.html')


@login_required(login_url='login')
def request_money(request):
    return render(request, 'payapp/request.html')


@login_required(login_url='login')
def help(request):
    return render(request, 'payapp/help.html')


@login_required(login_url='login')
def notifications(request):
    return render(request, 'payapp/notifications.html')
