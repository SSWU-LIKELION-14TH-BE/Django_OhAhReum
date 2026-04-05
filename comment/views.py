from django.shortcuts import redirect, get_object_or_404
from .models import Comment
from .forms import CommentForm
from article.models import Article
from django.contrib.auth.decorators import login_required

@login_required
def comment_create(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.article = article

            #대댓글 처리
            parent_id = request.POST.get('parent_id')
            if parent_id:
                comment.parent = Comment.objects.get(id=parent_id)

            comment.save()

    return redirect('article_detail', pk=article_pk)

def comment_like(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if request.user in comment.like_users.all():
        comment.like_users.remove(request.user)
    else:
        comment.like_users.add(request.user)

    return redirect('article_detail', pk=comment.article.pk)
