from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    nickname = models.CharField(max_length=30, default='anonymous')

    def __str__(self):
        return self.nickname

    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_permissions_set', blank=True)

    show_articles = models.BooleanField(default=True)
    show_comments = models.BooleanField(default=True)

class Guestbook(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='guestbooks'
    )  # 방명록 주인

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='written_guestbooks'
    )  # 방명록 작성자

    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    is_private = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.author} → {self.owner}"