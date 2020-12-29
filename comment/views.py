from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from sunnanblog.models import ArticlePost
from .forms import CommentForm


# 文章评论
@login_required()
def post_comment(request, aid):
    article = get_object_or_404(ArticlePost, id=aid)

    user = User.objects.get(username=request.user)

    # 处理 POST 请求
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            print(new_comment.article)
            new_comment.user = request.user
            print(new_comment.user)
            print(new_comment.body)
            new_comment.save()
            return HttpResponse('ok')
        else:
            print(comment_form.errors)
            return HttpResponse(comment_form.errors)
    # 处理错误请求
    else:
        return HttpResponse("发表评论仅接受POST请求。")


