from django.shortcuts import render, redirect
from django.http import HttpResponse
from sunnanblog.models import ArticlePost
from django.contrib.auth.models import User
from .form import ArticlePostForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import ArticlePost
from comment.models import Comment
import markdown


def index(req):
    activeList = ArticlePost.objects.order_by('-total_views')

    return render(req, 'sunnanblog/index.html', context={'article': activeList})


def article_list(req):
    articles = ArticlePost.objects.all()
    paginator = Paginator(articles, 7)
    page = req.GET.get('page', 1)

    articles = paginator.get_page(page)
    context = {'articles': articles, }
    return render(req, 'sunnanblog/article_list.html', context)


def about(req):
    return render(req, 'sunnanblog/about_me.html', context={})


def article_info(req, aid=1):
    article = ArticlePost.objects.get(id=aid)
    print('检查空格在哪加入', article.body)
    # 统计浏览量
    article.total_views += 1
    article.save(update_fields=['total_views'])
    print('输出文章作者', article.author.profile.avatar.url)

    # 获取该文章评论
    comment = Comment.objects.filter(article=aid).order_by("-created")
    print('输出此文章评论内容')
    print(comment)

    context = {'article': article, 'comment': comment, }
    return render(req, 'sunnanblog/article_info.html', context)


def article_create(req):
    if req.method == 'POST':
        article_post_form = ArticlePostForm(data=req.POST)
        print(article_post_form)
        if article_post_form.is_valid():
            new_article = article_post_form.save(commit=False)
            new_article.author = req.user
            new_article.save()
            return redirect('article_list')
        else:
            print('-'*50)
            print(article_post_form.errors)
            return HttpResponse('表单输入错误。')
    else:
        article_post_form = ArticlePostForm()
        context = {'article_post_form': article_post_form, }
        return render(req, 'sunnanblog/article_create.html', context)


@login_required()
def article_delete(req, aid):
    article = ArticlePost.objects.get(id=aid)
    if req.user != article.author:
        return HttpResponse("抱歉，你无权修改这篇文章。")
    if req.method == 'POST':
        article = ArticlePost.objects.get(id=aid)
        article.delete()
        return redirect('article_list')
    else:
        return HttpResponse("仅允许post请求")


@login_required()
def article_update(req, aid):
    # 获取需要修改的具体文章对象
    article = ArticlePost.objects.get(id=aid)
    if req.user != article.author:
        return HttpResponse("抱歉，你无权修改这篇文章。")
    # 判断用户是否为 POST 提交表单数据
    if req.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=req.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存新写入的 title、body 数据并保存
            article.title = req.POST['title']
            print('检查空格在哪加入的', req.POST['body'])
            article.body = req.POST['body']
            article.save()
            # 完成后返回到修改后的文章中。需传入文章的 id 值
            return redirect("article_info", aid=aid)
        # 如果数据不合法，返回错误信息
        else:
            print(article_post_form.errors)
            return HttpResponse("表单内容有误，请重新填写。")

    # 如果用户 GET 请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 赋值上下文，将 article 文章对象也传递进去，以便提取旧的内容
        context = {'article': article, 'article_post_form': article_post_form}
        # 将响应返回到模板中
        return render(req, 'sunnanblog/article_update.html', context)


def typing_game(request):
    return render(request, 'sunnanblog/typing_game.html')

