from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, ArticleImage
from .forms import ArticleForm
from django.contrib.auth.decorators import login_required

def article_list(request):
    articles = Article.objects.all().order_by('-created_at')
    return render(request, 'list.html', {'articles': articles})


def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'detail.html', {'article': article})


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

def article_like(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if request.user in article.like_users.all():
        article.like_users.remove(request.user)  # 좋아요 취소
    else:
        article.like_users.add(request.user)     # 좋아요 추가

    return redirect('article_detail', pk=pk)