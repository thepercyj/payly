from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import login as auth_login, authenticate
from .forms import RegistrationForm, LoginForm
from django.contrib.messages import error, get_messages
from django.contrib.auth.models import User


def register_user(request):
    """
    View function for user registration.

    :param request: The HTTP request.
    :return: Redirects to login page if registration is successful, otherwise renders the registration form.
    """
    add_superuser()
    if request.method == 'POST':
        form = RegistrationForm(False, request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            return render(request, 'register/register.html', {'title': 'Create an Account', 'form': form})
    else:
        return render(request, 'register/register.html', {'title': 'Create an Account', 'form': RegistrationForm()})


def login(request):
    """
    View function for user login.

    :param request: The HTTP request.
    :return: Redirects to home page if login is successful, otherwise renders the login form.
    """
    add_superuser()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            users = authenticate(username=username, password=password)
            if users is not None:
                auth_login(request, users)
                return HttpResponseRedirect('/')
            else:
                error(request, 'Invalid username or password')

        else:
            error(request, 'Invalid username or password')
            message_store = get_messages(request)
            context = {'title': 'Sign In',
                       'form': form, 'messages': message_store}
            return render(request, 'register/login.html', context)
    form = LoginForm()
    message_store = get_messages(request)
    context = {'title': 'Sign In',
               'form': form, 'messages': message_store}
    message_store.used = True
    return render(request, 'register/login.html', context)


def add_superuser():
    """
    Adds a superuser with default credentials if not already present in the database.
    """
    if not User.objects.filter(username='admin1').exists():
        User.objects.create_superuser(username='admin1', password='admin1')

