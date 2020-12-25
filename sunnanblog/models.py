from django.db import models
from django.contrib.auth.models import User
# timezone 用于处理时间相关事务。
from django.utils import timezone


class ArticlePost(models.Model):
    # 文章作者。参数 on_delete 用于指定数据删除的方式，避免两个关联表的数据不一致。
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # 文章标题。models.CharField 为字符串字段，用于保存较短的字符串，比如标题
    title = models.CharField(max_length=100)

    # 文章正文。保存大量文本使用 TextField
    body = models.TextField()

    # 文章创建时间。参数 default=timezone.now 指定其在创建数据时将默认写入当前的时间
    created = models.DateTimeField(default=timezone.now)

    # 文章更新时间。参数 auto_now=True 指定每次数据更新时自动写入当前时间
    updated = models.DateTimeField(auto_now=True)

    # 统计文章浏览量
    total_views = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'article'  # 定义数据库中表名
        ordering = ['id', '-created']  # 对象默认的排列顺序
        verbose_name = '文章'
        verbose_name_plural = '文章'

    def __str__(self):
        return self.title
