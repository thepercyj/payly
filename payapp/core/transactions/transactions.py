import uuid
from datetime import datetime

from django.http import HttpResponse

from payapp.models import Transaction, TransactionStatus
from django.db.models import Q
from django.contrib.auth.models import User
import thriftpy2
from thriftpy2.rpc import make_client
from thriftpy2.thrift import TException


timestamp_thrift = thriftpy2.load(
    'timestamp.thrift', module_name='timestamp_thrift')
Timestamp = timestamp_thrift.TimestampService


def get_trans_qs(user_id: int):
    return get_trans_id(user_id)


def get_trans_id(user_id: int, limit=50, sort='dsc', sortby='datetime') -> list:
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
    try:
        client = make_client(Timestamp, '127.0.0.1', 9090)
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

    except TException as e:
        return HttpResponse("An error occurred: {}".format(str(e)))


def get_transaction_id(id: int):
    return Transaction.objects.get(id=id)


def generate_tid():
    return uuid.uuid4()


def get_all_trans():
    return Transaction.objects.all()
