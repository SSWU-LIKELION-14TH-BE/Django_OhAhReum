from django.urls import path
from . import views

urlpatterns = [
    path('create/<int:article_pk>/', views.comment_create, name='comment_create'),
    path('like/<int:pk>/', views.comment_like, name='comment_like'),
]