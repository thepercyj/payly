import os
from random import choice
from django.contrib.auth.models import User
from django.core.validators import EmailValidator
from django import forms
from django.utils.translation import gettext_lazy as translate
from payapp.models import Currency
from .validation import user_email_exists, username_exists


def email_validator(email):
    """
    Validates the email address during user registration.

    :param email: The email address to validate.
    :raises: forms.ValidationError if the email address already exists.
    """
    if user_email_exists(email=email):
        raise forms.ValidationError('A user with this email id already exists, please use a different email address '
                                    'to sign up.')


def username_validator(username):
    """
    Validates the username during user registration.

    :param username: The username to validate.
    :raises: forms.ValidationError if the username already exists.
    """
    if username_exists(username=username):
        raise forms.ValidationError(translate('A user with that username already exists, please use a different '
                                              'username: %('
                                      'invalid_username)s'), params={
            'invalid_username': username
        })


def password_strength(password, is_superuser=False):
    """
    Validates the password strength during user registration.

    :param password: The password to validate.
    :param is_superuser: Boolean indicating if the user is a superuser. Default is False.
    :raises: forms.ValidationError if the password is too short.
    """
    if not is_superuser and len(password) < 8:
        raise forms.ValidationError('The provided password is too short, minimum password length is 5. Try again !')


def save_profile_picture():
    """
    Saves the user's profile picture.

    :return: Path to the saved profile picture.
    """
    profile_dir = 'media/profile/'
    path = 'profile/'
    profile_pics = os.listdir(profile_dir)
    return os.path.join(path, choice(profile_pics))


class RegistrationForm(forms.Form):
    """
    Form for user registration.

    :param is_superuser: Boolean indicating if the user is a superuser. Default is False.
    """
    firstname = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Eg: John'}), required=True, )
    lastname = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Eg: Wick'}), required=True)
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Eg: babayaga'}), required=True, validators=[username_validator])
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Eg: john.wick@gmail.com'}), required=True,
                            validators=[
                                email_validator, EmailValidator(message='Invalid email address provided')])
    password = forms.CharField(widget=forms.PasswordInput(
    ), required=True, validators=[password_strength])
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(), required=True)
    terms = forms.BooleanField(
        required=False, label='I accept Terms and conditions')
    is_superuser: bool = False

    def __init__(self, is_superuser: bool = False, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.is_superuser = is_superuser
        self.fields['currency'] = forms.ChoiceField(choices=Currency.choices, widget=forms.Select(), required=True)

    def clean(self):
        """
        Clean and validate form data.

        :raises: forms.ValidationError if passwords do not match or terms are not accepted.
        """
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match, please type it again.')

        if not self.is_superuser and cleaned_data.get('terms') == False:
            self.add_error(
                'terms', 'Please go through our terms and conditions first and accept it. ')

    def save(self, is_admin: bool = False):
        """
        Saves the user's registration information.

        :param is_admin: Boolean indicating if the user is an admin. Default is False.
        :return: The created user object.
        """
        username = self.cleaned_data['username']
        firstname = self.cleaned_data['firstname']
        lastname = self.cleaned_data['lastname']
        email = self.cleaned_data['email']
        password = self.cleaned_data['confirm_password']
        currency = self.cleaned_data['currency']
        superuser = User.objects.create_superuser if is_admin else User.objects.create_user
        user = superuser(username, email, password)
        user.first_name = firstname
        user.last_name = lastname
        user.wallet.currency = currency
        user.save()

        return user


class LoginForm(forms.Form):
    """
    Form for user login.
    """
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Eg: babayaga'}), required=True)
    password = forms.CharField(widget=forms.PasswordInput(
    ), required=True, validators=[password_strength])

    def clean(self):
        """
        Validates form fields.

        :raises forms.ValidationError: If form validation fails.
        """
        cleaned_data = super().clean()
        if not username_exists(cleaned_data['username']):
            self.add_error('username', 'The username does not match, please try again.')
