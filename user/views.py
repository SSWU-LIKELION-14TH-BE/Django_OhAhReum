from django.shortcuts import render, redirect
from django.contrib.auth import login

from user.models import CustomUser
from .forms import SignUpForm, LoginForm, GuestbookForm, ProfileUpdateForm
from django.contrib.auth import logout
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from article.models import Article
from comment.models import Comment
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth import update_session_auth_hash

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

@login_required
def mypage_view(request, user_id=None):
    target_user = get_object_or_404(CustomUser, id=user_id)
    is_owner = (request.user == target_user)


    # 글 / 댓글 공개 설정
    articles = (
        Article.objects.filter(author=target_user)
        if target_user.show_articles or is_owner
        else Article.objects.none()
    )

    comments = (
        Comment.objects.filter(author=target_user)
        if target_user.show_comments or is_owner
        else Comment.objects.none()
    )

    # 방명록 필터링
    if request.user.is_authenticated:
        guestbooks = target_user.guestbooks.filter(
            Q(is_private=False) |
            Q(author=request.user) |
            Q(owner=request.user)
        ).order_by('-created_at')
    else:
        guestbooks = target_user.guestbooks.filter(is_private=False)

    form = GuestbookForm()
    

    return render(request, 'mypage.html', {
        'target_user': target_user,
        'is_owner': is_owner,
        'articles': articles,
        'comments': comments,
        'guestbooks': guestbooks,
        'form': form,
    })

@login_required
def profile_update_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)

        if form.is_valid():
            user = form.save(commit=False)

            password = form.cleaned_data.get('password1')

            if password:
                user.set_password(password)

            user.save()

            # 비밀번호 변경 시 로그인 유지
            if password:
                update_session_auth_hash(request, user)
            messages.success(request, "회원정보가 수정되었습니다.")
            return redirect('mypage', user_id=request.user.id)

    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'profile_update.html', {'form': form})

@login_required
def guestbook_create_view(request, user_id):
    owner = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        form = GuestbookForm(request.POST)

        if form.is_valid():
            guestbook = form.save(commit=False)
            guestbook.author = request.user
            guestbook.owner = owner
            guestbook.save()

    return redirect('mypage', user_id=user_id)