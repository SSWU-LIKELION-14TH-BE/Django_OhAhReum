from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST) #상태정보가 있는 폼
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('signup') #signup페이지로 리다이렉트
    else:
        form = SignUpForm() #빈 새로운 폼

    return render(request, 'signup.html', {'form': form}) #기본적으로 get 메소드로 접근 = 페이지에 처음 들어가면 바로 새 폼 주어짐