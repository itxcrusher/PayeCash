from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    currency = forms.ChoiceField(choices=[('GBP', 'British Pound'), ('USD', 'US Dollar'), ('EUR', 'Euro')])

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'currency')
