from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True) #email필수

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'nickname', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    pass

class LogoutForm(forms.Form):
    pass

