from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, ArticleImage
from .forms import ArticleForm
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.db.models import Q, Count, F

def article_list(request):
    query = request.GET.get('q')
    search_type = request.GET.get('type')
    tech_ids = request.GET.getlist('tech')
    sort = request.GET.get('sort', 'latest')

    articles = Article.objects.all()

    # 검색
    if query:
        if search_type == 'all':
            articles = articles.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(comments__content__icontains=query) |
                Q(author__nickname__icontains=query)
            )

        elif search_type == 'content':
            articles = articles.filter(content__icontains=query)

        elif search_type == 'comment':
            articles = articles.filter(comments__content__icontains=query)

        elif search_type == 'author':
            articles = articles.filter(author__nickname__icontains=query)

        else:  # title
            articles = articles.filter(title__icontains=query)

    # 기술 스택 필터
    if tech_ids:
        articles = articles.filter(tech_stacks__id__in=tech_ids)
    articles = articles.distinct()

    # 좋아요 수 계산
    articles = articles.annotate(like_count=Count('like_users'))
    # 정렬
    if sort == 'popular':
        articles = articles.order_by('-like_count', '-created_at')
    else:
        articles = articles.order_by('-created_at')

    # 템플릿에 전달
    from .models import TechStack
    techs = TechStack.objects.all()

    return render(request, 'list.html', {
        'articles': articles,
        'query': query,
        'search_type': search_type,
        'selected_techs': list(map(int, tech_ids)),
        'techs': techs,
        'sort': sort,
    })


def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)

    cookie_name = f'viewed_{pk}'

    if not request.COOKIES.get(cookie_name):
        Article.objects.filter(pk=pk).update(views=F('views') + 1)

    response = render(request, 'detail.html', {'article': article})

    # 쿠키 설정 (1시간 재조회 방지)
    response.set_cookie(cookie_name, 'true', max_age=60*60)

    return response

@transaction.atomic  # 트랜잭션 시작
@login_required
def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)

        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            form.save_m2m()

            images = request.FILES.getlist('images')

            for img in images:
                ArticleImage.objects.create(
                    article=article,
                    image=img
                )

            return redirect('article_detail', pk=article.pk)

    else:
        form = ArticleForm()

    return render(request, 'create.html', {'form': form})

@login_required
def article_like(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if article.like_users.filter(pk=request.user.pk).exists():
        article.like_users.remove(request.user)  # 좋아요 취소
    else:
        article.like_users.add(request.user)     # 좋아요 추가

    return redirect('article_detail', pk=pk)

@login_required
@transaction.atomic
def article_update(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if request.user != article.author:
        messages.error(request, "작성자만 수정할 수 있습니다.")
        return redirect('article_detail', pk=pk)

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)

        if form.is_valid():
            form.save()

            # 삭제할 이미지 처리
            delete_images = request.POST.getlist('delete_images')
            if delete_images:
                ArticleImage.objects.filter(id__in=delete_images, article=article).delete()

            # 새 이미지 추가
            images = request.FILES.getlist('images')
            for img in images:
                ArticleImage.objects.create(
                    article=article,
                    image=img
                )

            return redirect('article_detail', pk=pk)

    else:
        form = ArticleForm(instance=article)

    return render(request, 'create.html', {
        'form': form,
        'article': article  # 템플릿에서 기존 이미지 넘김
    })

@login_required
def article_delete(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if request.user != article.author:
        messages.error(request, "작성자만 삭제할 수 있습니다.")
        return redirect('article_detail', pk=pk)

    article.delete()
    return redirect('article_list')