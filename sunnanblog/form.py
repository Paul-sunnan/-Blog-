from django import forms
# 引入文章模型
from .models import ArticlePost


class ArticlePostForm(forms.ModelForm):
    class Meta:
        model = ArticlePost
        fields = ('title', 'body')


