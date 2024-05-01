import decimal
import thriftpy2
from django.db import transaction
from thriftpy2.rpc import make_client
from thriftpy2.thrift import TException
from datetime import datetime
from django.http import HttpResponse
from walletapp.models import Wallet
from walletapp.core.wallet import add_money, check_balance, deduct_money
from payapp.models import TransactionStatus, TransferRequest
from django.contrib.auth.models import User
from payapp.core.transactions.transactions import create_transaction, generate_tid
from django.db.models import Q
from notificationapp.core.notifications import notify, NotificationType

timestamp_thrift = thriftpy2.load(
    'timestamp.thrift', module_name='timestamp_thrift')
Timestamp = timestamp_thrift.TimestampService


def transfer_money(sender_id, receiver_id, amount, currency):
    """
    Transfers money from one user to another.

    :param sender_id: int
        The ID of the user sending the money.
    :param receiver_id: int
        The ID of the user receiving the money.
    :param amount: decimal.Decimal or str
        The amount of money to transfer.
    :param currency: str
        The currency of the transfer.
    :return: bool
        Returns True if the transfer is successful.
    """
    if not type(amount) == 'Decimal':
        amount = decimal.Decimal(amount)
    check_balance(sender_id, amount, currency)
    # raise TransferException('Some random transfer exception')
    return transfer_money_id(sender_id, receiver_id, amount, currency)


@transaction.atomic
def transfer_money_id(sender_id, receiver_id, amount, currency, notified: bool = True):
    """
    Transfers money from one user to another, given their IDs.

    :param sender_id: int
        The ID of the user sending the money.
    :param receiver_id: int
        The ID of the user receiving the money.
    :param amount: decimal.Decimal or str
        The amount of money to transfer.
    :param currency: str
        The currency of the transfer.
    :param notified: bool, optional
        Indicates whether to notify users about the transfer (default is True).
    :return: bool
        Returns True if the transfer is successful.
    """

    sender = User.objects.get(id=sender_id)
    receiver = User.objects.get(id=receiver_id)

    sender_wallet = Wallet.objects.get(user_id=sender.id)
    sender_balance = deduct_money(sender_wallet, amount, currency)

    receiver_wallet = Wallet.objects.get(user_id=receiver.id)
    receiver_balance = add_money(receiver_wallet, amount, currency)

    tid = generate_tid()

    create_transaction(tid, sender, receiver, TransactionStatus.SUCCESS, amount, currency, sender_balance)

    if notified:
        notify(sender_id, 'Money Transferred',
               f'You have transferred {amount} {currency} to {receiver.first_name} {receiver.last_name}',
               type=NotificationType.TRANSACTION_SUCCESS)
        notify(receiver_id, 'Money Recieved',
               f'You have recieved {amount} {currency} from {sender.first_name} {sender.last_name}',
               type=NotificationType.MONEY_RECIEVED)
    return True


@transaction.atomic
def add_transfer_req(sender_id: int, receiver_id: int, amount, currency):
    """
    Adds a transfer request for money from one user to another.

    :param sender_id: int
        The ID of the user sending the transfer request.
    :param receiver_id: int
        The ID of the user receiving the transfer request.
    :param amount: decimal.Decimal or str
        The amount of money requested.
    :param currency: str
        The currency of the transfer request.
    """

    try:
        client = make_client(Timestamp, '127.0.0.1', 10000)
        timestamp = datetime.fromtimestamp(int(str(client.getCurrentTimestamp())))
        rid = generate_tid()
        sender = User.objects.get(id=sender_id)
        receiver = User.objects.get(id=receiver_id)
        tr_request = TransferRequest(
            rid=rid,
            sender=sender,
            receiver=receiver,
            source=sender,
            amount=decimal.Decimal(amount),
            currency=currency,
            datetime=timestamp,
        )
        tr_request.save()
        notify(sender_id, 'Transfer Request Sent',
               f'You have requested {receiver.first_name} an amount of {amount} {currency}.',
               type=NotificationType.MONEY_REQUEST)
        notify(receiver_id, 'Transfer Request Recieved',
               f'{receiver.first_name} has requested an amount of {amount} {currency}.',
               type=NotificationType.MONEY_REQUEST)

    except TException as e:
        return HttpResponse("An error occurred: {}".format(str(e)))


def get_transfer_req_id_qs(user_id: int) -> list:
    """
    Retrieves a list of transfer requests for a user.

    :param user_id: int
        The ID of the user.
    :return: list
        A list of TransferRequest objects.
    """

    return list(get_transfer_req_id(user_id))


def get_transfer_req_id(user_id: int, group='all') -> list:
    if group == 'sent':
        query = Q(sender_id__exact=user_id)
    elif group == 'recieved':
        query = Q(receiver_id__exact=user_id)
    else:
        query = Q(sender_id__exact=user_id) | Q(receiver_id__exact=user_id)
    transactions = TransferRequest.objects.filter(
        query
    )
    return transactions.all()


def transfer_req_id(rid: int):
    return TransferRequest.objects.get(id=rid)


def withdraw_trans_req(rid: int):
    """
    Withdraws a transfer request.

    :param rid: int
        The ID of the transfer request to withdraw.
    :return: bool
        Returns True if the withdrawal is successful.
    """

    request = transfer_req_id(rid)
    request.delete()

    return True


def approve_trans_req(rid: int):
    """
    Approves a transfer request and transfers the money.

    :param rid: int
        The ID of the transfer request to approve.
    :return: bool
        Returns True if the approval and transfer are successful.
    """
    request = transfer_req_id(rid)
    transfer_money_id(sender_id=request.receiver.id, receiver_id=request.sender.id, amount=request.amount,
                      currency=request.currency)
    request.delete()
    return True


def deny_trans_req(rid: int):
    """
    Denies a transfer request.

    :param rid: int
        The ID of the transfer request to deny.
    :return: bool
        Returns True if the denial is successful.
    """
    request = transfer_req_id(rid)
    request.delete()
    return True
