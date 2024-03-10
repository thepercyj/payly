from django.contrib.auth.models import User
from django.core.validators import EmailValidator
from django import forms
from django.utils.translation import gettext_lazy as translate
from .validation import user_email_exists, username_exists


# function that validates email
def email_validator(email):
    if user_email_exists(email=email):
        raise forms.ValidationError('A user with this email id already exists, please use a different email address '
                                    'to sign up.')


# function that validates username
def username_validator(username):
    if username_exists(username=username):
        raise forms.ValidationError(translate('A user with that username already exists, please use a different '
                                              'username: %('
                                      'invalid_username)s'), params={
            'invalid_username': username
        })


# function that checks password strength, must not be less than 8 as per standards.
def password_strength(password):
    if len(password) < 8:
        raise forms.ValidationError('The provided password is too short, minimum password length is 8. Try again !')


# Registration form to register new users.
class RegistrationForm(forms.Form):
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

    # Adding custom clear function for form validations

    def clean(self):
        cleaned_data = super().clean()

        # Checks if the password entered by the user twice is same or not.
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        # print error stating passwords do not match.
        if password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match, please type it again.')

        if not self.is_superuser and cleaned_data.get('terms') == False:
            self.add_error(
                'terms', 'Please go through our terms and conditions first and accept it. ')

    def save(self, is_admin: bool = False):
        username = self.cleaned_data['username']
        firstname = self.cleaned_data['firstname']
        lastname = self.cleaned_data['lastname']
        email = self.cleaned_data['email']
        password = self.cleaned_data['confirm_password']
        superuser = User.objects.create_superuser if is_admin else User.objects.create_user
        user = superuser(username, email, password)
        user.first_name = firstname
        user.last_name = lastname
        user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Eg: babayaga'}), required=True)
    password = forms.CharField(widget=forms.PasswordInput(
    ), required=True, validators=[password_strength])

    # checking enable to verify if the supplied username matches in the database or not.
    def clean(self):
        cleaned_data = super().clean()
        if not username_exists(cleaned_data['username']):
            self.add_error('username', 'The username does not match, please try again.')
