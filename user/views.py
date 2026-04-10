from django.shortcuts import render, redirect
from django.contrib.auth import login

from user.models import CustomUser
from .forms import SignUpForm
from .forms import LoginForm
from django.contrib.auth import logout
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST) #상태정보가 있는 폼
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home') #home페이지로 리다이렉트
    else:
        form = SignUpForm() #빈 새로운 폼

    return render(request, 'signup.html', {'form': form}) #기본적으로 get 메소드로 접근 = 페이지에 처음 들어가면 바로 새 폼 주어짐

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home') # home페이지로 리다이렉트
    else:
        form = LoginForm() #빈 새로운 폼

    return render(request, 'login.html', {'form': form})

def home_view(request):
    return render(request, 'home.html')

def logout_view(request):
    logout(request)
    return redirect('login')


class CustomPasswordResetView(PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')

from django.contrib.auth.views import (
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'