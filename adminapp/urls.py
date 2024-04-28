from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='admin'),
    path('all-users/', views.index_users, name='all-users'),
    path('all-transactions/', views.index_transactions, name='all-transactions')
]

htmxpatterns = [
    path('htmx/get-all-users/', views.all_users, name='get-all-users'),
    path('htmx/get-all-transactions/',
         views.all_transactions, name='get-all-transactions'),
    path('htmx/all-user-trans-list/', views.all_user_trans_list, name='all-user-trans-list'),
    path('htmx/add-admin/', views.add_admin, name='add-admin'),
]

urlpatterns += htmxpatterns
