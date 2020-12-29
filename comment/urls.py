from django.urls import path
from . import views

app_name = 'comment'

urlpatterns = [
    # 发表评论
    path('post_comment/<int:aid>/', views.post_comment, name='post_comment'),
]