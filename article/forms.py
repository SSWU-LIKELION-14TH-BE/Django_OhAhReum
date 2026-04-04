from django import forms 
from .models import Article, TechStack

class ArticleForm(forms.ModelForm):
    tech_stacks = forms.ModelMultipleChoiceField(
        queryset=TechStack.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Article
        fields = ['title', 'content', 'tech_stacks', 'github_url']