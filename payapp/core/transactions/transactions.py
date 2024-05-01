import uuid
import thriftpy2
from datetime import datetime
from django.http import HttpResponse
from payapp.models import Transaction, TransactionStatus
from django.db.models import Q
from django.contrib.auth.models import User
from thriftpy2.rpc import make_client
from thriftpy2.thrift import TException


timestamp_thrift = thriftpy2.load(
    'timestamp.thrift', module_name='timestamp_thrift')
Timestamp = timestamp_thrift.TimestampService


def get_trans_qs(user_id: int):
    """
    Retrieves a queryset of transactions for a user.

    :param user_id: int
        The ID of the user.
    :return: QuerySet
        A queryset containing the transactions for the user.
    """
    return get_trans_id(user_id)


def get_trans_id(user_id: int, limit=50, sort='dsc', sortby='datetime') -> list:
    """
    Retrieves a list of transactions for a user.

    :param user_id: int
        The ID of the user.
    :param limit: int, optional
        The maximum number of transactions to retrieve (default is 50).
    :param sort: str, optional
        The sorting order ('asc' for ascending, 'dsc' for descending) (default is 'dsc').
    :param sortby: str, optional
        The field to sort by (default is 'datetime').
    :return: list
        A list of Transaction objects.
    """

    transactions = Transaction.objects.filter(
        Q(sender_id__exact=user_id) |
        Q(receiver_id__exact=user_id)
    )

    sortby = sortby or 'datetime'
    if sort == 'asc':
        orderby = sortby
    else:
        orderby = f'-{sortby}'
    return transactions.all().order_by(orderby)[:limit]


def unique_trans_id(user_id: int):
    """
    Retrieves unique transactions for a user.

    :param user_id: int
        The ID of the user.
    :return: list
        A list of unique User objects involved in transactions with the user.
    """
    transactions = Transaction.objects.filter(
        Q(sender_id__exact=user_id) |
        Q(receiver_id__exact=user_id)
    )
    unique = []

    for t in transactions:
        if not t.receiver in unique:
            unique.append(t.receiver)
    return unique


def create_transaction(transaction_id: str, sender: User, receiver: User, status: TransactionStatus, amount, currency,
                       balance):
    """
    Creates a transaction and saves it to the database.

    :param transaction_id: str
        The ID of the transaction.
    :param sender: User
        The sender of the transaction.
    :param receiver: User
        The receiver of the transaction.
    :param status: TransactionStatus
        The status of the transaction.
    :param amount: decimal.Decimal or str
        The amount of money involved in the transaction.
    :param currency: str
        The currency of the transaction.
    :param balance: decimal.Decimal or str
        The balance after the transaction.
    """

    try:
        client = make_client(Timestamp, '127.0.0.1', 10000)
        timestamp = datetime.fromtimestamp(int(str(client.getCurrentTimestamp())))
        transaction = Transaction(
            tid=transaction_id,
            sender=sender,
            receiver=receiver,
            amount=amount,
            currency=currency,
            status=status,
            balance=balance,
            datetime=timestamp,
        )
        transaction.save()
        print(f"The {sender} is sending money to , {receiver} and is successfully saved in database.")
    except TException as e:
        return HttpResponse("An error occurred: {}".format(str(e)))


def get_transaction_id(id: int):
    """
    Retrieves a transaction by ID.

    :param id: int
        The ID of the transaction.
    :return: Transaction
        The Transaction object.
    """
    return Transaction.objects.get(id=id)


def generate_tid():
    """
    Generates a unique transaction ID.

    :return: str
        A unique transaction ID.
    """
    return uuid.uuid4()


def get_all_trans():
    """
    Retrieves all transactions.

    :return: QuerySet
        A queryset containing all transactions.
    """
    return Transaction.objects.all()
