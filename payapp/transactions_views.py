# from django.contrib.auth.decorators import login_required
# from django.http import Http404
# from django.shortcuts import render
#
# from payapp.core.transactions.transactions import get_all_trans, get_trans_id, get_transaction_id
#
#
# @login_required(login_url='login')
# def transaction(request):
#     notifications = get_notifications_for_user(request.user.id)
#     if request.method == 'GET':
#         return render(request, 'transaction/layout/list.html', {'count': len(notifications)})
#     raise Http404()
#
#
# @login_required(login_url='login')
# def list(request):
#     if request.method == 'GET':
#         limit = int(request.GET.get('limit')
#                     ) if request.GET.get('limit') else 100
#         sort = request.GET.get('sort')
#         sortby = request.GET.get('sortby')
#
#         type = request.GET.get('type') or 'user'
#         transactions = []
#
#         if type == 'all':
#             transactions = get_all_trans()
#         else:
#             transactions = get_trans_id(
#                 request.user.id, limit=limit, sort=sort, sortby=sortby)
#
#         if len(transactions) == 0:
#             context = {
#                 'title': 'Oops !! You have not made any transactions yet.',
#                 'message': 'Please return after completing a transaction to view details.'
#             }
#             return render(request, 'transaction/partials/empty.html', context)
#
#         for tr in transactions:
#             if tr.sender.id == request.user.id:
#                 tr.type = 'DEBIT'
#             else:
#                 tr.type = 'CREDIT'
#         context = {
#             'transactions': transactions,
#             'type': type
#         }
#         return render(request, 'transaction/partials/transaction-table.html', context)
#     raise Http404()
#
#
# @login_required(login_url='login')
# def transaction_detail(request):
#     if request.method == 'GET':
#         tid = request.GET.get('tid')
#         transaction = get_transaction_id(tid)
#         if transaction.sender.id == request.user.id:
#             transaction.type = 'DEBIT'
#         else:
#             transaction.type = 'CREDIT'
#         context = {
#             't': transaction,
#         }
#         return render(request, 'transaction/partials/transaction-detail.html', context)
#     raise Http404()
