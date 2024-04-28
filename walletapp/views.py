from django.shortcuts import render
from payapp.core.banking.bank import get_user_bank_acc
from payapp.models import UserProfile
from popup.popup import PopupHttpResponse
from walletapp.core.wallet import add_money, change_currency
from decimal import Decimal
from .forms import AddMoneyForm, ChangeCurrencyForm
from popup.views import no_view
from django.contrib.auth.decorators import login_required


# Create your views here.
# index page of wallet app
@login_required(login_url='login')
def wallet(request):
    user_profile = UserProfile.objects.get(user=request.user)
    context = {
        'accounts': get_user_bank_acc(request.user.id),
        'user_profile': user_profile
    }
    return render(request, 'walletapp/layout/index.html', context)


# Http response with AddmoneyForm
@login_required(login_url='login')
def get_add_money(request):
    # handle form submition
    if request.method == 'POST':
        form = AddMoneyForm(request.POST)

        # form validation
        if form.is_valid():
            amt = request.POST.get('amount')

            # access local api to add money to wallet
            add_money(request.user.wallet, Decimal(
                amt), request.user.wallet.currency)

            # return a success Toast message
            return PopupHttpResponse(True, 'Money Credited', f'{amt} added successfully to your wallet')

        # invalid form handle
        else:
            context = {
                'form': form
            }
            return render(request, 'walletapp/modal/add_money_amount_form.html', context)

    # id tag in GET request denoted user has browsed to this url via user search
    if 'id' in request.GET:
        context = {
            'form': AddMoneyForm()
        }
        return render(request, 'walletapp/modal/add_money_amount_form.html', context)

    # fetch all available bank accounts of the user
    accounts = get_user_bank_acc(request.user.id)

    # handle no banks accounts listed case with an empty partial page response
    if len(accounts) <= 0:
        return no_view(request, 'No Banks added', 'You have not added any accounts yet.')
    context = {
        'accounts': accounts
    }
    return render(request, 'walletapp/modal/add_money_bank_select.html', context)


# Http response with Change Money Form
@login_required(login_url='login')
def get_change_currency(request):
    form = ChangeCurrencyForm(request.user.wallet.currency)

    # handle post request for submitted forms
    if request.method == 'POST':
        form = ChangeCurrencyForm(request.user.wallet.currency, request.POST)

        # check if form is valid
        if form.is_valid():
            currency = form.cleaned_data['currency']
            # use local api to change currency
            change_currency(request.user.wallet, currency)
            # return success Toast
            return PopupHttpResponse(True, 'Currency Changed',
                                     f'You have successfully changed default currency to {currency}')
        # return error toast on invalid form
        return PopupHttpResponse(False, 'Error Occured',
                                 'Some error occured while changing your default currency. Please try again later')

    # return new form for new GET requests
    return render(request, 'walletapp/modal/change_currency.html', {'form': form})


# Http response for Wallet Card
@login_required(login_url='login')
def get_balance(request):
    # return ToastHttpResponse(False)
    return render(request, 'walletapp/modal/wallet_balance_card.html')


# Http response for Currency Card
@login_required(login_url='login')
def get_currency(request):
    user_profile = UserProfile.objects.get(user=request.user)
    # return ToastHttpResponse(False)
    return render(request, 'walletapp/modal/currency_card.html', {'user_profile': user_profile})
