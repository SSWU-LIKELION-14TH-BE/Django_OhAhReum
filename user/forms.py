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

class PasswordResetForm(forms.Form):
    username = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=150)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned = super().clean()

        if cleaned.get('password1') != cleaned.get('password2'):
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")

        return cleaned