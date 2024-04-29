from django.shortcuts import redirect, render
from django.contrib.auth import logout as leave
from django.contrib.auth.decorators import login_required

from notificationapp.models import Notification
from payapp.core.transactions.transactions import unique_trans_id
from notificationapp.core.notifications import get_user_notifications
from payapp.core.account.account import profile_id
from payapp.models import UserProfile
from popup.views import no_view


# Create your views here.
def alert(request):
    context = {
        'success': request.GET.get('success') or False,
        'title': request.GET.get('title'),
        'message': request.GET.get('message')
    }
    return render(request, 'main/modal/alert.html', context)


@login_required(login_url='login')
def dashboard(request):

    if request.user.is_superuser:
        return redirect('admin')

    context = {
        'title': 'Dashboard',
    }
    return render(request, 'main/layout/dashboard.html', context)


@login_required(login_url='login')
def recent_transfers(request):
    r_transfers = unique_trans_id(request.user.id)
    if r_transfers is None or len(r_transfers) == 0:
        return no_view(request, 'Oops !! You have not made any transactions yet.',
                          'Please return after completing a transaction to view details.')
    context = {
        'r_transfers': r_transfers,
    }
    return render(request, 'main/modal/recent-transfer-list.html', context)


def logout(request):
    leave(request)
    return redirect('login')
