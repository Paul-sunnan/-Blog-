from django.db import models
from django.contrib.auth.models import User
from sunnanblog.models import ArticlePost
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey


# 博文的评论
class Comment(models.Model):
    article = models.ForeignKey(
        ArticlePost,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.body[:20]

    def get_absolute_url(self):
        return reverse('article_info', args=[self.id])

