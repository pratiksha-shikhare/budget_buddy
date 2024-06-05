from django import forms
from .models import CommonExpense, Payment

class CommonExpenseForm(forms.ModelForm):
    class Meta:
        model = CommonExpense
        fields = ['user','amount', 'description']

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['description']
        widgets = {
            'description': forms.Select(choices=Payment.PAYMENT_DESC, attrs={'class': 'form-control'}),
        }

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(max_length=20)