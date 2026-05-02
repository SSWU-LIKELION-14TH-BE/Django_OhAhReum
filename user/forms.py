from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Guestbook

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True) #email필수

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'nickname', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    pass

class LogoutForm(forms.Form):
    pass

class ProfileUpdateForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
        label="새 비밀번호"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
        label="새 비밀번호 확인"
    )

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'nickname',
            'show_articles',
            'show_comments',
        ]

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')

        if p1 or p2:
            if p1 != p2:
                raise forms.ValidationError("비밀번호가 일치하지 않습니다.")

        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)

        password = self.cleaned_data.get('password1')

        if password:
            user.set_password(password)

        if commit:
            user.save()

        return user
    
class GuestbookForm(forms.ModelForm):
    class Meta:
        model = Guestbook
        fields = ['content', 'is_private']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3})
        }