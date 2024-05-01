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
    """
    Deducts the specified amount from the wallet balance.

    :param wallet: The wallet from which the money will be deducted.
    :param amount: The amount to deduct.
    :param currency: The currency of the amount.
    :return: The updated balance of the wallet.
    """
    currency = currency or wallet.currency
    base_currency_amt = amount * decimal.Decimal(conversion[currency][wallet.currency])
    wallet.balance -= decimal.Decimal(base_currency_amt)
    wallet.save()
    return wallet.balance


def add_money(wallet: Wallet, amount: decimal.Decimal, currency):
    """
    Adds the specified amount to the wallet balance.

    :param wallet: The wallet to which the money will be added.
    :param amount: The amount to add.
    :param currency: The currency of the amount.
    :return: The updated balance of the wallet.
    """
    currency = currency or wallet.currency
    base_currency_amt = amount * decimal.Decimal(conversion[currency][wallet.currency])
    wallet.balance += decimal.Decimal(base_currency_amt)
    wallet.save()
    return wallet.balance


def check_balance(sender_id, amount: decimal.Decimal, currency):
    """
    Checks if the sender has sufficient balance for the transaction.

    :param sender_id: The ID of the sender.
    :param amount: The amount to be transferred.
    :param currency: The currency of the amount.
    :return: A dictionary containing the current balance and currency if the balance is sufficient, else raises a TransferException.
    """
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


def convert(amount: decimal.Decimal, from_currency: Currency, to_currency: Currency):
    """
    Converts the specified amount from one currency to another.

    :param amount: The amount to convert.
    :param from_currency: The currency to convert from.
    :param to_currency: The currency to convert to.
    :return: The converted amount.
    """
    return amount * decimal.Decimal(conversion[from_currency][to_currency])


def change_currency(user_wallet: Wallet, currency: Currency):
    """
    Changes the currency of the user's wallet.

    :param user_wallet: The user's wallet.
    :param currency: The new currency.
    :return: True if the currency is changed successfully, else False.
    """
    user_wallet.balance = convert(user_wallet.balance, user_wallet.currency, currency)
    user_wallet.currency = currency
    user_wallet.save()
    return True
