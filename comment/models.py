from django.db import models
from django.conf import settings
from article.models import Article

class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')

    content = models.TextField()

    #대댓글은 자기 자신 참조, 없으면 일반 댓글
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:20]