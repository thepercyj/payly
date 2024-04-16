from django.urls import path
from . import views

urlpatterns = [
    path('account/', views.account, name='account'),
    path('banking/', views.banking, name='banking'),
    path('transaction/', views.transaction, name='transaction'),
    path('send-money/', views.send_money, name='send-money'),
    path('request-money/', views.request_money, name='request-money'),
    path('transfer-requests/', views.transfer_requests, name='transfer-requests'),

]

htmxpatterns = [

    # Account
    path('htmx/edit-profile/', views.edit_profile, name='edit-profile'),
    path('htmx/change-password/', views.change_password, name='change-password'),


    # Banking
    path('htmx/create-bank-account', views.create_bank_acc, name='create-bank-account'),
    path('htmx/list-bank-account', views.list_bank_acc, name='list-bank-account'),
    path('htmx/remove-bank-account', views.remove_bank_acc, name='remove-bank-account'),
    path('htmx/list-transfer-requests', views.list_transfer_requests, name='list-transfer-requests'),
    path('htmx/confirm-transfer-withdrawal', views.confirm_transfer_withdrawal, name='confirm-transfer-withdrawal'),
    path('htmx/confirm-transfer-approval', views.confirm_transfer_approval, name='confirm-transfer-approval'),
    path('htmx/confirm-transfer-denial', views.confirm_transfer_denial, name='confirm-transfer-denial'),
    path('htmx/request-withdrawal', views.request_withdrawal, name='request-withdrawal'),
    path('htmx/approve-transfer', views.approve_transfer, name='approve-transfer'),
    path('htmx/deny-transfer', views.deny_transfer, name='deny-transfer'),
    path('htmx/send-money-details', views.send_money_details, name='send-money-details'),
    path('htmx/request-money-details', views.request_money_details, name='request-money-details'),

    # Transactions
    path('htmx/transaction-list', views.transaction_list, name='transaction-list'),
    path('htmx/transaction-detail', views.transaction_detail, name='transaction-detail'),
    path('htmx/detail-type', views.detail_type, name='detail-type'),


]

urlpatterns += htmxpatterns