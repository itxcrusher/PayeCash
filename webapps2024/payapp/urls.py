from django.urls import path
from .views import AccountDetailView, HomeView, SendPaymentView, TransactionListView, AllAccountsView, AllTransactionsView

app_name = 'payapp'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('account/', AccountDetailView.as_view(), name='account_detail'),
    path('send-payment/', SendPaymentView.as_view(), name='send_payment'),
    path('transactions/', TransactionListView.as_view(), name='transaction_list'),
    path('admin/accounts/', AllAccountsView.as_view(), name='all_accounts'),  # For admins
    path('admin/transactions/', AllTransactionsView.as_view(), name='all_transactions'),  # For admins
]
