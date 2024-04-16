from django import forms
from payapp.models import Currency


# A custom validator to limit transactions of large amounts
def amount_validator(amount):
    if int(amount) > 10000:
        raise forms.ValidationError('Sorry, you cannot perform transactions of more than 10000 at once.')


# Form to add money to user wallet
class AddMoneyForm(forms.Form):
    amount = forms.DecimalField(decimal_places=2, max_digits=15, widget=forms.TextInput(
        attrs={'placeholder': 'Eg: $100.00'}), validators=[amount_validator])


# form to change default currency of user wallet
class ChangeCurrencyForm(forms.Form):
    currency = forms.ChoiceField(choices=Currency.choices, required=True, widget=forms.Select(
        attrs={'placeholder': 'Default'},
    ))

    def __init__(self, current_currency: Currency, *args, **kwargs):
        super(ChangeCurrencyForm, self).__init__(*args, **kwargs)
        # set initial currency to current currency
        self.fields['currency'].initial = current_currency
