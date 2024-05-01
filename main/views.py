from django.shortcuts import redirect, render
from django.contrib.auth import logout as leave
from django.contrib.auth.decorators import login_required
from payapp.core.transactions.transactions import unique_trans_id
from popup.views import no_view


def alert(request):
    """
    Renders the alert modal with success status, title, and message.

    :param request: HttpRequest
        The request object containing information about the current HTTP request.
    :type request: HttpRequest
    :return: HttpResponse
        The rendered alert modal.
    """
    context = {
        'success': request.GET.get('success') or False,
        'title': request.GET.get('title'),
        'message': request.GET.get('message')
    }
    return render(request, 'main/modal/alert.html', context)


@login_required(login_url='login')
def dashboard(request):
    """
    Renders the dashboard page for the authenticated user.

    :param request: HttpRequest
        The request object containing information about the current HTTP request.
    :type request: HttpRequest
    :return: HttpResponse
        The rendered dashboard page.
    """

    if request.user.is_superuser:
        return redirect('admin')

    context = {
        'title': 'Dashboard',
    }
    return render(request, 'main/layout/dashboard.html', context)


@login_required(login_url='login')
def recent_transfers(request):
    """
    Renders the page displaying recent transfers for the authenticated user.

    :param request: HttpRequest
        The request object containing information about the current HTTP request.
    :type request: HttpRequest
    :return: HttpResponse
        The rendered page displaying recent transfers.
    """

    r_transfers = unique_trans_id(request.user.id)
    if r_transfers is None or len(r_transfers) == 0:
        return no_view(request, 'Oops !! You have not made any transactions yet.',
                          'Please return after completing a transaction to view details.')
    context = {
        'r_transfers': r_transfers,
    }
    return render(request, 'main/modal/recent-transfer-list.html', context)


def logout(request):
    """
    Logs out the user and redirects to the login page.

    :param request: HttpRequest
        The request object containing information about the current HTTP request.
    :type request: HttpRequest
    :return: HttpResponseRedirect
        Redirects to the login page.
    """
    leave(request)
    return redirect('login')
