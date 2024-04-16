from payapp.models import Currency
from walletapp.models import Wallet
from walletapp.core.exception import TransferException
import decimal

conversion = {
    'USD': {
        'GBP': 0.79,
        'EUR': 0.92,
        'USD': 1.0
    },
    'GBP': {
        'GBP': 1.0,
        'EUR': 1.17,
        'USD': 1.26
    },
    'EUR': {
        'GBP': 0.86,
        'EUR': 1.0,
        'USD': 1.08
    }
}


def deduct_money(wallet: Wallet, amount: decimal.Decimal, currency):
    currency = currency or wallet.currency
    base_currency_amt = amount * decimal.Decimal(conversion[currency][wallet.currency])
    wallet.balance -= decimal.Decimal(base_currency_amt)
    wallet.save()
    return wallet.balance


def add_money(wallet: Wallet, amount: decimal.Decimal, currency):
    currency = currency or wallet.currency
    base_currency_amt = amount * decimal.Decimal(conversion[currency][wallet.currency])
    wallet.balance += decimal.Decimal(base_currency_amt)
    wallet.save()
    return wallet.balance


def check_balance(sender_id, amount: decimal.Decimal, currency):
    s_wallet = Wallet.objects.get(user_id=sender_id)
    s_balance = s_wallet.balance * decimal.Decimal(conversion[s_wallet.currency][currency])
    required_balance = amount * decimal.Decimal(conversion[currency][s_wallet.currency])

    if amount > s_balance:
        raise TransferException(
            f'Insufficient funds: You require {required_balance} in {s_wallet.currency} to proceed with this '
            f'transaction.')
    return {
        'balance': s_balance - required_balance,
        'currency': s_wallet.currency,
        'success': True
    }


def convert(amount: decimal.Decimal, source: Currency, to: Currency):
    return amount * decimal.Decimal(conversion[source][to])


def change_currency(user_w: Wallet, currency: Currency):
    user_w.balance = convert(user_w.balance, user_w.currency, currency)
    user_w.currency = currency
    user_w.save()
    return True
