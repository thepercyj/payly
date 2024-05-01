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
    path('modal/edit-profile/', views.edit_profile, name='edit-profile'),
    path('modal/change-password/', views.change_password, name='change-password'),

    # Banking
    path('modal/create-bank-account', views.create_bank_acc, name='create-bank-account'),
    path('modal/list-bank-account', views.list_bank_acc, name='list-bank-account'),
    path('modal/remove-bank-account', views.remove_bank_acc, name='remove-bank-account'),
    path('modal/list-transfer-requests', views.list_transfer_requests, name='list-transfer-requests'),
    path('modal/confirm-transfer-withdrawal', views.confirm_transfer_withdrawal, name='confirm-transfer-withdrawal'),
    path('modal/confirm-transfer-approval', views.confirm_transfer_approval, name='confirm-transfer-approval'),
    path('modal/confirm-transfer-denial', views.confirm_transfer_denial, name='confirm-transfer-denial'),
    path('modal/request-withdrawal', views.request_withdrawal, name='request-withdrawal'),
    path('modal/approve-transfer', views.approve_transfer, name='approve-transfer'),
    path('modal/deny-transfer', views.deny_transfer, name='deny-transfer'),
    path('modal/send-money-details', views.send_money_details, name='send-money-details'),
    path('modal/request-money-details', views.request_money_details, name='request-money-details'),

    # Transactions
    path('modal/transaction-list', views.transaction_list, name='transaction-list'),
    path('modal/transaction-detail', views.transaction_detail, name='transaction-detail'),
    path('modal/detail-type', views.detail_type, name='detail-type'),

]

urlpatterns += htmxpatterns
