from django import forms
from .models import CommonExpense

class CommonExpenseForm(forms.ModelForm):
    class Meta:
        model = CommonExpense
        fields = ['user','amount', 'description']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(max_length=20)