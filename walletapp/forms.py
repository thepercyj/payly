from django import forms
from payapp.models import Currency


def amount_validator(amount):
    """
    Validates the amount to ensure it does not exceed the maximum limit.

    :param amount: The amount to validate.
    :raises forms.ValidationError: If the amount exceeds the maximum limit.
    """
    if int(amount) > 10000:
        raise forms.ValidationError('Sorry, you cannot perform transactions of more than 10000 at once.')


class AddMoneyForm(forms.Form):
    """
    Form for adding money to the wallet.

    """
    amount = forms.DecimalField(decimal_places=2, max_digits=15, widget=forms.TextInput(
        attrs={'placeholder': 'Eg: $100.00'}), validators=[amount_validator])


class ChangeCurrencyForm(forms.Form):
    """
    Form for changing the currency of the wallet.

    """
    currency = forms.ChoiceField(choices=Currency.choices, required=True, widget=forms.Select(
        attrs={'placeholder': 'GBP'},
    ))

    def __init__(self, current_currency: Currency, *args, **kwargs):
        """
        Initializes the ChangeCurrencyForm.

        :param current_currency: The current currency of the wallet.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        """
        super(ChangeCurrencyForm, self).__init__(*args, **kwargs)
        self.fields['currency'].initial = current_currency
