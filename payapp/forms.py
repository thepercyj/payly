from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.contrib.auth.models import User
from register.validation import user_email_exists, username_exists
from walletapp.core.exception import TransferException
from walletapp.core.wallet import check_balance
from .core.account.wallet import wallet_profile_id
from .core.banking.bank import add_bank_acc
from .core.banking.search import search_by_identifier
from .models import Currency
from decimal import Decimal
from crispy_forms.helper import FormHelper


class EditUserProfileForm(forms.Form):
    """
    A form for editing user profile information.

    :ivar current_user: User
        The current user.
    """
    firstname = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Eg: John'}))
    lastname = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Eg: Doe'}))
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Eg: JohnDoe123', }))
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Eg: john.doe@gmail.com'}),
                            validators=[
                                EmailValidator(message='Invalid email')])

    current_user: User = None

    def __init__(self, current_user: User, *args, **kwargs):
        super(EditUserProfileForm, self).__init__(*args, **kwargs)
        if current_user:
            self.fields['firstname'].initial = current_user.first_name
            self.fields['lastname'].initial = current_user.last_name
            self.fields['username'].initial = current_user.username
            self.fields['email'].initial = current_user.email
            self.current_user = current_user

    def save(self):
        self.current_user.username = self.cleaned_data['username']
        self.current_user.first_name = self.cleaned_data['firstname']
        self.current_user.last_name = self.cleaned_data['lastname']
        self.current_user.email = self.cleaned_data['email']
        self.current_user.save()
        return self.current_user


# validate email field
def email_validator(email):
    # make sure the given email doesn't already exist in the database
    if not user_email_exists(email=email):
        raise forms.ValidationError('A user exists with this email id.')


# validate username field
def username_validator(username):
    # make sure the given username doesn't already exist in the database
    if not username_exists(username=username):
        raise forms.ValidationError('A user exists with username : %(invalid_username)s', params={
            'invalid_username': username
        })


class RequestUserForm(forms.Form):
    """
    A form for requesting user information.

    :ivar identifier: str
        The identifier for searching users.
    :ivar amount: decimal.Decimal
        The amount for the request.
    :ivar currency: str
        The currency for the request.
    """
    identifier = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'username, email, firstname or lastname'}), required=True, validators=[])
    amount = forms.DecimalField(decimal_places=2, max_digits=20, widget=forms.TextInput(
        attrs={'placeholder': 'Eg: 2,000,000.00'}))
    currency = forms.ChoiceField(choices=Currency.choices, widget=forms.Select(
        attrs={'placeholder': 'username, email, firstname or lastname'}
    ))


def EmptyValidator(identifier):
    if identifier is None or len(identifier) <= 0:
        raise forms.ValidationError('This field cannot be empty')


class SearchUserForm(forms.Form):
    """
    A form for searching users.

    :ivar tag: str
        The form tag.
    :ivar identifier: str
        The identifier for searching users.
    """

    tag = forms.CharField(widget=forms.HiddenInput(attrs={'value': 'search'}), required=True)
    identifier = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Search by Name, Email or UserID'}), required=True,
        validators=[EmptyValidator], label=None)

    def search(self):
        string = self.cleaned_data['identifier']
        results = search_by_identifier(string)
        if len(results) <= 0:
            self.add_error('identifier',
                           forms.ValidationError('Oops !! user having similar name, email or username not found'))
        return results

    def __init__(self, *args, **kwargs):
        super(SearchUserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False


class SendForm(forms.Form):
    """
    A form for sending money.

    :ivar sender: User
        The sender of the money.
    :ivar wallet: Wallet
        The wallet of the sender.
    """

    amount = forms.DecimalField(decimal_places=2, widget=forms.NumberInput(
        attrs={'placeholder': 'Eg: £100.00',
               'type': 'number'
               }), required=True, validators=[], label=None)
    currency = forms.ChoiceField(choices=Currency.choices, widget=forms.Select(
        attrs={'placeholder': 'Select Currency',
               }
    ))

    wallet = None

    def __init__(self, sender, *args, **kwargs):

        super(SendForm, self).__init__(*args, **kwargs)
        self.sender = sender
        wallet = wallet_profile_id(self.sender)
        print(f'sender (at constr): {sender}')
        self.fields['currency'].initial = wallet.currency

    def clean(self):
        data = super().clean()
        amount = data.get('amount')
        curr = data.get('currency')
        print(f'sender: {self.sender}, amount: {amount}, curr: {curr}')
        if amount and curr and self.sender:

            try:
                check_balance(self.sender, Decimal(amount), curr)
                return data
            except TransferException as e:
                print(f'transfer-exception {e}')
                self.add_error('amount', ValidationError(str(e.message)))
            except Exception as e:
                print(f'normal-exception {e}')
                self.add_error('amount', ValidationError(str(e)))
        else:
            self.add_error('currency', ValidationError('Insufficient Parameters'))


class RequestForm(forms.Form):
    """
    A form for requesting money.

    :ivar sender: User
        The sender of the request.
    :ivar wallet: Wallet
        The wallet of the sender.
    """
    amount = forms.DecimalField(decimal_places=2, widget=forms.NumberInput(
        attrs={'placeholder': 'Eg: £100.00',
               'type': 'number'
               }), required=True, validators=[], label=None)
    currency = forms.ChoiceField(choices=Currency.choices, widget=forms.Select(
        attrs={'placeholder': 'Select Currency',
               }
    ))

    wallet = None

    def __init__(self, sender, *args, **kwargs):
        super(RequestForm, self).__init__(*args, **kwargs)
        self.sender = sender
        wallet = wallet_profile_id(self.sender)
        self.fields['currency'].initial = wallet.currency


class BankAccForm(forms.Form):
    """
    A form for adding bank account information.

    :ivar bank: str
        The name of the bank.
    :ivar account_no: str
        The account number.
    """
    bank = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Bank Name'}), required=True, validators=[])
    account_no = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Account Number'}), required=True, validators=[])

    def save(self, user):
        data = super().clean()
        name = data['bank']
        no = data['account_no']
        try:
            return add_bank_acc(name, no, user)
        except Exception as e:
            self.add_error('account_no', ValidationError(str(e)))
