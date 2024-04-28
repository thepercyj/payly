import json
import os
from random import choice

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from .forms import EditUserProfileForm
from popup.popup import PopupHttpResponse
from notificationapp.core.notifications import get_user_notifications
from walletapp.core.exception import TransferException
from .forms import BankAccForm, SearchUserForm, RequestForm, SendForm
from payapp.core.banking.bank import get_user_bank_acc, delete_bank_acc, get_acc_id
from popup.views import no_view
from payapp.core.banking.search import search_by_id
from payapp.core.banking.transfers import add_transfer_req, withdraw_trans_req, approve_trans_req, deny_trans_req, \
    transfer_money, get_transfer_req_id, transfer_req_id
from payapp.core.transactions.transactions import get_all_trans, get_trans_id, get_transaction_id
from .models import UserProfile


############################### ACCOUNT VIEWS START ###############################
@login_required(login_url='login')
def account(request):
    user_profile = UserProfile.objects.get(user=request.user)
    notifications = get_user_notifications(request.user.id)
    return render(request, 'payapp/account/layout/index.html', {'count': len(notifications), 'user_profile': user_profile})


@login_required(login_url='login')
def edit_profile(request):
    form = EditUserProfileForm(request.user)

    if request.method == 'POST':
        form = EditUserProfileForm(request.user, request.POST)
        if form.is_valid():
            new_user = form.save()
            return PopupHttpResponse(True, 'User Profile Changed', 'Your profile has been successfully changed.')

    context = {
        'form': form,
        'user': request.user
    }
    return render(request, 'payapp/account/modal/edit-profile.html', context)


@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Your password was successfully updated!')
            return redirect('login')  # Redirect to success page
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'payapp/account/modal/change_password.html', {'form': form})


############################### ACCOUNT VIEWS END ###############################


############################### BANKING VIEWS START ###############################
@login_required(login_url='login')
def banking(request):
    notifications = get_user_notifications(request.user.id)
    return render(request, 'payapp/banking/layout/index.html', {'count': len(notifications)})


@login_required(login_url='login')
def create_bank_acc(request):
    form = BankAccForm()

    if request.method == 'POST':
        form = BankAccForm(request.POST)
        if form.is_valid():
            account = form.save(request.user)
            return PopupHttpResponse(success=True, title='New Bank Account Added',
                                     message=f'{account.bank} has been added to your account.')
    return render(request, 'payapp/banking/modal/create-account.html', {'form': form})


@login_required(login_url='login')
def list_bank_acc(request):
    if not request.method == 'GET':
        return PopupHttpResponse(success=False, title='Error Occurred', message='Not Allowed')

    user_id = request.GET.get('user_id')
    if not user_id:
        return PopupHttpResponse(success=False, title='Error Occurred', message='Not Allowed')

    accounts = get_user_bank_acc(user_id)
    if len(accounts) <= 0:
        return no_view(request, 'No Accounts Added', 'You have not added any accounts yet.')

    context = {
        'accounts': accounts
    }
    return render(request, 'payapp/banking/modal/list-accounts.html', context)


@login_required(login_url='login')
def remove_bank_acc(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        delete_bank_acc(id)
        return PopupHttpResponse(success=True, title='Bank Account Removed',
                                 message='Bank account has been successfully removed from your account')

    context = {
        'account': get_acc_id(id=request.GET.get('id'))
    }
    return render(request, 'payapp/banking/modal/confirm-remove.html', context)


@login_required(login_url='login')
def transfer_requests(request):
    notifications = get_user_notifications(request.user.id)
    if request.method == 'GET':
        return render(request, 'payapp/banking/layout/tr-requests.html', {'count': len(notifications)})
    raise Http404()


@login_required(login_url='login')
def list_transfer_requests(request):
    if request.method == 'GET':
        group = request.GET.get('group') if request.GET.get(
            'group') is not None else 'all'
        results = get_transfer_req_id(request.user.id, group)
        context = {
            'transfer_req': results,
            'group': group,
            'count': len(results)
        }
        print(len(results))
        return render(request, 'payapp/banking/modal/list-transfer-requests.html', context)
    return HttpResponse('No content')


@login_required(login_url='login')
def confirm_transfer_withdrawal(request):
    if request.method == 'GET':
        context = {
            'rid': request.GET.get('rid')
        }
        return render(request, 'payapp/banking/modal/withdraw-confirm.html', context)
    return HttpResponse('No content')


@login_required(login_url='login')
def confirm_transfer_approval(request):
    if request.method == 'GET':
        context = {
            'tr': transfer_req_id(request.GET.get('rid'))
        }
        return render(request, 'payapp/banking/modal/approval-confirm.html', context)
    return HttpResponse('No content')


@login_required(login_url='login')
def confirm_transfer_denial(request):
    if request.method == 'GET':
        context = {
            'tr': transfer_req_id(request.GET.get('rid'))
        }
        return render(request, 'payapp/banking/modal/denial-confirm.html', context)
    return HttpResponse('No content')


@login_required(login_url='login')
def request_withdrawal(request):
    if request.method == 'GET':
        rid = request.GET.get('rid')
        tr_rq = transfer_req_id(rid)
        withdraw_trans_req(rid)
        return PopupHttpResponse(True, 'Request Withdrawn',
                                 f'Transfer request of {tr_rq.currency} {tr_rq.amount} was successfully withdrawn')

    return HttpResponse('No content')


@login_required(login_url='login')
def approve_transfer(request):
    if request.method == 'GET':
        try:
            rid = request.GET.get('rid')
            tr_rq = transfer_req_id(rid)
            approve_trans_req(rid)
            return PopupHttpResponse(True, 'Money Transferred',
                                     f'You have successfully transferred {tr_rq.amount} {tr_rq.currency} to {tr_rq.receiver.first_name}.')
        except TransferException as te:
            context = {
                'message': te.message
            }
            return render(request, 'payapp/banking/modal/send-failure.html', context)
        except Exception as e:
            return HttpResponse(f'Transaction Failed: {str(e)}')

    return HttpResponse('No content')


@login_required(login_url='login')
def deny_transfer(request):
    if request.method == 'GET':
        try:
            rid = request.GET.get('rid')
            tr_rq = transfer_req_id(rid)
            deny_trans_req(rid)
            return PopupHttpResponse(True, 'Transfer Request Declined',
                                     f'You have declined the transfer request from {tr_rq.recipient.first_name} for an amount of {tr_rq.currency} {tr_rq.amount} successfully')
        except TransferException as te:
            context = {
                'message': te.message
            }
            return render(request, 'payapp/banking/modal/send-failure.html', context)
        except Exception as e:
            return PopupHttpResponse(False, 'Error Occurred', f'{str(e)}')

    return HttpResponse('No content')


@login_required(login_url='login')
def send_money(request):
    notifications = get_user_notifications(request.user.id)
    form = SearchUserForm()
    results = []
    if request.method == 'GET':
        if 'identifier' in request.GET:
            form = SearchUserForm(request.GET)

        if form.is_valid():
            results = form.search()

        return render(request, 'payapp/banking/layout/send-money.html',
                      {'form': form, 'search_results': results, 'count': len(notifications)})
    else:
        raise Http404()


@login_required(login_url='login')
def send_money_details(request):
    print(f'user: {request.user}')
    if request.method == 'POST' and 'confirm' not in request.POST:
        receiver = search_by_id(request.POST.get('receiver'))
        form = SendForm(request.user.id, request.POST)
        if form.is_valid():
            context = {
                'form': form,
                'receiver': receiver,
                'sender': request.user,
                'amount': request.POST.get('amount'),
                'currency': request.POST.get('currency')
            }
            return render(request, 'payapp/banking/modal/send-money-confirm.html', context)
        context = {
            'form': form,
            'receiver': receiver
        }
        return render(request, 'payapp/banking/modal/send-money-details.html', context)

    elif request.method == 'POST' and 'confirm' in request.POST:

        try:
            sender_id = request.POST.get('sender')
            receiver_id = request.POST.get('receiver')
            amount = request.POST.get('amount')
            currency = request.POST.get('currency')
            receiver = search_by_id(receiver_id)
            transfer_money(sender_id, receiver_id, amount, currency)
            return HttpResponse(status=204, headers={
                'HX-Trigger': json.dumps({
                    'popup': {
                        'success': True,
                        'title': 'Money Transferred',
                        'message': f'You have successfully transferred {amount} {currency} to {receiver.first_name}.'
                    }
                })
            })

        except TransferException as te:
            context = {
                'message': te.message
            }
            return render(request, 'payapp/banking/modal/send-money-failure.html', context)
        except Exception as e:
            return HttpResponse(f'Transaction Failed: {str(e)}')

    elif 'receiver' not in request.GET:
        raise Http404()
    receiver = search_by_id(request.GET.get('receiver'))
    context = {
        'form': SendForm(request.user.id),
        'receiver': receiver
    }
    return render(request, 'payapp/banking/modal/send-money-details.html', context)


@login_required(login_url='login')
def detail_type(request):
    if 'type' in request.GET:
        if request.GET.get('type') == 'request':
            return request_money_details(request)
        if request.GET.get('type') == 'send':
            return send_money_details(request)
    raise Http404()


@login_required(login_url='login')
def request_money(request):
    notifications = get_user_notifications(request.user.id)
    form = SearchUserForm()
    results = []
    if request.method == 'GET':
        if 'identifier' in request.GET:
            form = SearchUserForm(request.GET)

        if form.is_valid():
            results = form.search()

        return render(request, 'payapp/banking/layout/request-money.html',
                      {'form': form, 'search_results': results, 'count': len(notifications)})
    else:
        raise Http404()


@login_required(login_url='login')
def request_money_details(request):
    print(f'user: {request.user}')
    if request.method == 'POST' and 'confirm' not in request.POST:
        receiver = search_by_id(request.POST.get('receiver'))
        form = RequestForm(request.user.id, request.POST)
        if form.is_valid():
            context = {
                'form': form,
                'receiver': receiver,
                'sender': request.user,
                'amount': request.POST.get('amount'),
                'currency': request.POST.get('currency')
            }
            return render(request, 'payapp/banking/modal/request-money-confirm.html', context)
        context = {
            'form': form,
            'receiver': receiver
        }
        return render(request, 'payapp/banking/modal/request-money-details.html', context)

    elif request.method == 'POST' and 'confirm' in request.POST:

        try:
            sender_id = request.POST.get('sender')
            receiver_id = request.POST.get('receiver')
            amount = request.POST.get('amount')
            currency = request.POST.get('currency')
            add_transfer_req(sender_id, receiver_id, amount, currency)
            context = {
                'form': RequestForm(request.user.id, request.POST),
                'receiver': search_by_id(receiver_id),
                'sender': request.user,
                'amount': amount,
                'currency': currency
            }
            return render(request, 'payapp/banking/modal/request-money-success.html', context)
        except TransferException as te:
            context = {
                'message': te.message
            }
            return render(request, 'payapp/banking/modal/request-money-failure.html', context)
        except Exception as e:
            return HttpResponse(f'Transaction Failed: {str(e)}')

    elif 'receiver' not in request.GET:
        raise Http404()
    receiver = search_by_id(request.GET.get('receiver'))
    context = {
        'form': RequestForm(request.user.id),
        'receiver': receiver
    }
    return render(request, 'payapp/banking/modal/request-money-details.html', context)


###############################  BANKING VIEWS END ###############################


############################### TRANSACTIONS VIEWS START ###############################

@login_required(login_url='login')
def transaction(request):
    notifications = get_user_notifications(request.user.id)
    if request.method == 'GET':
        return render(request, 'payapp/transaction/layout/list.html', {'count': len(notifications)})
    raise Http404()


@login_required(login_url='login')
def transaction_list(request):
    if request.method == 'GET':
        limit = int(request.GET.get('limit')
                    ) if request.GET.get('limit') else 100
        sort = request.GET.get('sort')
        sortby = request.GET.get('sortby')

        type = request.GET.get('type') or 'user'
        transactions = []

        if type == 'all':
            transactions = get_all_trans()
        else:
            transactions = get_trans_id(
                request.user.id, limit=limit, sort=sort, sortby=sortby)

        if len(transactions) == 0:
            context = {
                'title': 'Oops !! You have not made any transactions yet.',
                'message': 'Please return after completing a transaction to view details.'
            }
            return render(request, 'payapp/transaction/modal/empty.html', context)

        for tr in transactions:
            if tr.sender.id == request.user.id:
                tr.type = 'DEBIT'
            else:
                tr.type = 'CREDIT'
        context = {
            'transactions': transactions,
            'type': type
        }
        return render(request, 'payapp/transaction/modal/transaction-table.html', context)
    raise Http404()


@login_required(login_url='login')
def transaction_detail(request):
    if request.method == 'GET':
        tid = request.GET.get('tid')
        transaction = get_transaction_id(tid)
        if transaction.sender.id == request.user.id:
            transaction.type = 'DEBIT'
        else:
            transaction.type = 'CREDIT'
        context = {
            't': transaction,
        }
        return render(request, 'payapp/transaction/modal/transaction-detail.html', context)
    raise Http404()

###############################  TRANSACTIONS VIEWS END ###############################
