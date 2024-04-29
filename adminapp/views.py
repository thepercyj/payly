from django.shortcuts import render

from notificationapp.models import Notification
from payapp.core.transactions.transactions import get_trans_id
from payapp.models import UserProfile
from .core.data import get_no_of_transactions, get_no_of_users, get_all_transactions, get_all_users
from .decorators import admin_required
from popup.views import no_view
from register.forms import RegistrationForm
from popup.popup import PopupHttpResponse
from .core.view_utils import redirect_if_not_super_user


@admin_required(login_url='login')
def index(request):
    context = {
        'users': get_no_of_users(),
        'success_transactions': get_no_of_transactions(True),
        'pending_transactions': get_no_of_transactions(False),
    }
    return render(request, 'adminapp/layout/dashboard.html', context)


@admin_required(login_url='login')
def all_users(request):
    # redirect_if_not_super_user(request)
    users = get_all_users(request.user) or []
    if users is None or len(users) == 0:
        return no_view(request, 'No users Found',
                          'We didnot find any users yet. Whenever a new user registers, this page will show them.')
    context = {
        'users': users,
    }
    return render(request, 'adminapp/modal/users_list.html', context)


@admin_required(login_url='login')
def all_user_trans_list(request):
    # redirect_if_not_super_user(request)
    users = get_all_users(request.user) or []
    if users is None or len(users) == 0:
        return no_view(request, 'No users Found',
                       'We didnot find any users yet. Whenever a new user registers, this page will show them.')
    context = {
        'users': users,
    }
    return render(request, 'adminapp/modal/transaction_users_list.html', context)


@admin_required(login_url='login')
def all_transactions(request):
    # redirect_if_not_super_user(request)
    limit = int(request.GET.get('limit')
                ) if request.GET.get('limit') else 100
    sort = request.GET.get('sort')
    sortby = request.GET.get('sortby')
    type = request.GET.get('type')
    user = request.GET.get('user_id')
    if user is not None:
        user = int(user)

    if type == 'users':
        transactions = get_all_transactions()
    else:
        transactions = get_trans_id(user, limit=limit, sort=sort, sortby=sortby)

    if transactions is None or len(transactions) == 0:
        return no_view(request, 'No Transactions Found',
                          'We didnot find any transactions yet. Whenever a user completes a transaction, this page will show them.')

    for tr in transactions:
        print("THis is sender & request",tr.sender.id, request.user.id)
        if tr.sender.id == user:
            tr.type = 'DEBIT'
        else:
            tr.type = 'CREDIT'

    context = {
        'transactions': transactions,
        'type': type,
    }
    return render(request, 'adminapp/modal/transactions_list.html', context)


@admin_required(login_url='login')
def index_transactions(request):
    # redirect_if_not_super_user(request)
    return render(request, 'adminapp/layout/all-transactions.html')


@admin_required(login_url='login')
def index_users(request):
    # redirect_if_not_super_user(request)
    return render(request, 'adminapp/layout/all-users.html')


@admin_required(login_url='login')
def add_admin(request):
    # redirect_if_not_super_user(request)
    form = RegistrationForm(is_superuser=True)
    if request.method == 'POST':
        form = RegistrationForm(True, request.POST)
        if form.is_valid():
            try:
                user = form.save(is_admin=True)
                return PopupHttpResponse(True, 'Admin User Created',
                                         f'You have successfully created an admin account for {user.first_name} {user.last_name}')
            except Exception as e:
                return PopupHttpResponse(False, 'Error Occured',
                                         f'Some error occured while creating this user. Plese try again later {str(e)}')

        else:
            return render(request, 'adminapp/modal/add-admin.html', {'form': form})

    return render(request, 'adminapp/modal/add-admin.html', {'form': form})
