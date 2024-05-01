from django.shortcuts import render
from payapp.core.banking.bank import get_user_bank_acc
from popup.popup import PopupHttpResponse
from walletapp.core.wallet import add_money, change_currency
from decimal import Decimal
from .forms import AddMoneyForm, ChangeCurrencyForm
from popup.views import no_view
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def wallet(request):
    """
    View function to display the wallet of the logged-in user.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The HTTP response containing the wallet information.

    """
    context = {
        'accounts': get_user_bank_acc(request.user.id),
    }
    return render(request, 'walletapp/layout/index.html', context)


@login_required(login_url='login')
def get_add_money(request):
    """
    View function to handle adding money to the user's wallet.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The HTTP response for adding money to the wallet.

    """
    if request.method == 'POST':
        form = AddMoneyForm(request.POST)

        if form.is_valid():
            amt = request.POST.get('amount')

            add_money(request.user.wallet, Decimal(
                amt), request.user.wallet.currency)

            return PopupHttpResponse(True, 'Money Credited', f'{amt} added successfully to your wallet')

        else:
            context = {
                'form': form
            }
            return render(request, 'walletapp/modal/add_money_amount_form.html', context)

    if 'id' in request.GET:
        context = {
            'form': AddMoneyForm()
        }
        return render(request, 'walletapp/modal/add_money_amount_form.html', context)

    accounts = get_user_bank_acc(request.user.id)

    if len(accounts) <= 0:
        return no_view(request, 'No Banks added', 'You have not added any accounts yet.')
    context = {
        'accounts': accounts
    }
    return render(request, 'walletapp/modal/add_money_bank_select.html', context)


@login_required(login_url='login')
def get_change_currency(request):
    """
    View function to handle changing the default currency of the user's wallet.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The HTTP response for changing the currency.

    """
    form = ChangeCurrencyForm(request.user.wallet.currency)

    if request.method == 'POST':
        form = ChangeCurrencyForm(request.user.wallet.currency, request.POST)

        if form.is_valid():
            currency = form.cleaned_data['currency']
            change_currency(request.user.wallet, currency)
            return PopupHttpResponse(True, 'Currency Changed',
                                     f'You have successfully changed default currency to {currency}')
        return PopupHttpResponse(False, 'Error Occured',
                                 'Some error occured while changing your default currency. Please try again later')

    return render(request, 'walletapp/modal/change_currency.html', {'form': form})


@login_required(login_url='login')
def get_balance(request):
    """
    View function to display the balance of the user's wallet.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The HTTP response containing the wallet balance.

    """
    return render(request, 'walletapp/modal/wallet_balance_card.html')


@login_required(login_url='login')
def get_currency(request):
    """
    View function to display the currency of the user's wallet.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The HTTP response containing the wallet currency.

    """
    return render(request, 'walletapp/modal/currency_card.html')
