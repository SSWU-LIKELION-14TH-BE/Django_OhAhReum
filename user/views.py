from django.shortcuts import render, redirect
from django.contrib.auth import login

from user.models import CustomUser
from .forms import SignUpForm
from .forms import LoginForm
from django.contrib.auth import logout
from .forms import PasswordResetForm

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

def password_reset_view(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            try:
                user = CustomUser.objects.get(username=username, email=email)
                user.set_password(password)
                user.save()
                return redirect('login')
            except CustomUser.DoesNotExist:
                form.add_error(None, "일치하는 사용자가 없습니다.")
    else:
        form = PasswordResetForm()

    return render(request, 'password_reset.html', {'form': form})