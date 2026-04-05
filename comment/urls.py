from django.urls import path
from . import views

urlpatterns = [
    path('create/<int:article_pk>/', views.comment_create, name='comment_create'),
]