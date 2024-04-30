from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class SendPaymentForm(forms.Form):
    receiver = forms.CharField(max_length=150, required=True)
    amount = forms.DecimalField(max_digits=10, decimal_places=2, required=True)
    currency = forms.ChoiceField(choices=[('USD', 'USD'), ('EUR', 'EUR'), ('GBP', 'GBP')], required=True)

    def clean_receiver(self):
        receiver_username = self.cleaned_data['receiver']
        try:
            user = User.objects.get(username=receiver_username)
            return user
        except User.DoesNotExist:
            raise ValidationError("Receiver not found.")
