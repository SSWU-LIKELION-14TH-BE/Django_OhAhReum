from django.shortcuts import redirect, get_object_or_404
from .models import Comment
from .forms import CommentForm
from article.models import Article
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def comment_create(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.article = article

            # 대댓글 처리
            parent_id = request.POST.get('parent_id')
            if parent_id:
                parent_comment = get_object_or_404(Comment, id=parent_id, article=article)
                comment.parent = parent_comment

            comment.save()

    return redirect('article_detail', pk=article_pk)

@login_required
def comment_like(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if comment.like_users.filter(pk=request.user.pk).exists():
        comment.like_users.remove(request.user)
    else:
        comment.like_users.add(request.user)

    return redirect('article_detail', pk=comment.article.pk)

@login_required
def comment_update(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if request.user != comment.author:
        messages.error(request, "작성자만 수정할 수 있습니다.")
        return redirect('article_detail', pk=comment.article.pk)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)

        if form.is_valid():
            form.save()

    return redirect('article_detail', pk=comment.article.pk)


@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if request.user != comment.author:
        messages.error(request, "작성자만 삭제할 수 있습니다.")
        return redirect('article_detail', pk=comment.article.pk)

    article_pk = comment.article.pk
    comment.delete()

    return redirect('article_detail', pk=article_pk)