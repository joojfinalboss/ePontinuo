from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from bootstrap_daterangepicker import widgets, fields

class SignupForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ['username', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class DemoForm(forms.Form):
    # Date Range Fields
    Selecione_a_Data_para_Filtrar = fields.DateRangeField()




