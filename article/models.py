from django.db import models
from django.conf import settings

class Article(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField()

    tech_stacks = models.ManyToManyField('TechStack', blank=True)

    github_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_articles', blank=True)

    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
    
    
class ArticleImage(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='articles/', null=True, blank=True)


class TechStack(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name