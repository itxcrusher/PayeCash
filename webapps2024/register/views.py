from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from payapp.models import Account

from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm
from payapp.models import Account

class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')  # Adjust as necessary
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        currency = form.cleaned_data.get('currency')
        Account.objects.create(user=self.object, balance=0, currency=currency)
        return response
