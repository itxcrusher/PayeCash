from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from payapp.forms import SendPaymentForm
from .models import Account, Transaction
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views import View
from django.shortcuts import redirect, render
from .models import Transaction, Account
from django.contrib.auth.models import User
from django.db import transaction
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models


class SendPaymentView(View):
    template_name = 'payapp/send_payment.html'

    def get(self, request, *args, **kwargs):
        form = SendPaymentForm()
        return render(request, self.template_name, {'form': form})

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = SendPaymentForm(request.POST)
        if form.is_valid():
            receiver_user = form.cleaned_data['receiver']
            amount = form.cleaned_data['amount']
            currency = form.cleaned_data['currency']
            sender_account = request.user.account
            receiver_account = Account.objects.get(user=receiver_user)
            
            # Here you would also handle currency conversion
            if sender_account.balance >= amount:
                sender_account.balance -= amount
                receiver_account.balance += amount
                sender_account.save()
                receiver_account.save()
                Transaction.objects.create(sender=request.user, receiver=receiver_user, amount=amount, currency=currency)
                # Redirect to a new URL:
                return redirect('payapp:home')
            else:
                form.add_error(None, "Insufficient funds")
        
        return render(request, self.template_name, {'form': form})
class AccountDetailView(DetailView):
    model = Account
    template_name = 'payapp/account_detail.html'
    context_object_name = 'account'

    def get_queryset(self):
        # Ensure users can only view their own account details
        return self.model.objects.filter(user=self.request.user)
    


class AllAccountsView(UserPassesTestMixin, ListView):
    model = Account
    template_name = 'admin/all_accounts.html'
    context_object_name = 'accounts'

    def test_func(self):
        return self.request.user.is_superuser

class AllTransactionsView(UserPassesTestMixin, ListView):
    model = Transaction
    template_name = 'admin/all_transactions.html'
    context_object_name = 'transactions'

    def test_func(self):
        return self.request.user.is_superuser

class AdminSignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'admin/register_new_admin.html'
    success_url = reverse_lazy('admin:index')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    


class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'payapp/transaction_list.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        # Return transactions where the user is either the sender or the receiver
        return Transaction.objects.filter(models.Q(sender=self.request.user) | models.Q(receiver=self.request.user)).order_by('-timestamp')

class HomeView(LoginRequiredMixin, DetailView):
    model = Account
    template_name = 'payapp/home.html'
    context_object_name = 'account'

    def get_object(self):
        # Ensure the user can only access their own account details
        return Account.objects.get(user=self.request.user)
