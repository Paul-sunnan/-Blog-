from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .form import UserLoginForm, UserSignupForm, ProfileForm
from .models import Profile, EmailVeriRecord
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

import random
import requests
from django_redis import get_redis_connection
from django.core.mail import send_mail
from paul7sk8 import settings

from django.core.cache import cache


def user_login(req, ):
    if req.method == 'POST':
        user_login_form = UserLoginForm(data=req.POST)
        print(user_login_form)
        if user_login_form.is_valid():
            print('数据通过')
            data = user_login_form.cleaned_data
            print(data['username'], data['password'])
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                print('密码正确')
                login(req, user)
                return redirect('/')
            else:
                print('密码错误')
                return HttpResponse('登录失败')
        else:
            return HttpResponse('输入错误')
    else:
        user_login_form = UserLoginForm()
        context = {
            'form': user_login_form,
        }
        return render(req, 'userprofile/login.html', context)


def user_logout(req):
    logout(req)
    return redirect('login')


def user_signup(req):
    if req.method == 'POST':
        user_register_form = UserSignupForm(data=req.POST)
        code = req.POST.get('code')
        email = req.POST.get('email')
        cache = get_redis_connection()
        if cache.get(email + '_code'):
            email_code = cache.get(email + '_code')
        else:
            return HttpResponse("验证码已过期，请重新申请验证码")
        if code == email_code.decode(encoding="utf-8"):
            if user_register_form.is_valid():
                new_user = user_register_form.save(commit=False)
                new_user.set_password(user_register_form.cleaned_data['password'])
                new_user.save()
                login(req, new_user)
                return redirect('home')
            else:
                print(user_register_form.errors)
                return HttpResponse("注册表单输入有误。请重新输入~")
        else:
            return HttpResponse("验证码输入错误")
    else:
        user_register_form = UserSignupForm()
        context = {'form': user_register_form}
        return render(req, 'userprofile/signup.html', context)


def user_mail_send(req):
    # 使用的ajax请求
    if req.method == "POST":
        email = req.POST.get('email')

        code = random.randint(1001, 9999)
        # 存储验证码
        cache = get_redis_connection()
        cache.set(email+'_code', code, 300)

        if email:
            # 发送email
            result_code = send_mail('孙楠Blog网站注册验证码', '您好，您在站点:www.paul7sk8.cn 的账号注册验证码："' + str(code) + '"，5分钟内有效 。', settings.EMAIL_HOST_USER, [email, ])
            EmailVeriRecord.objects.create(email=email, code=code, email_type='注册邮件')
            if result_code == 1:
                return HttpResponse('ok')
            else:
                return HttpResponse('no')
        else:
            return HttpResponse('no')
    else:
        return HttpResponse('no')


@login_required()
def profile_edit(req):
    user = User.objects.get(username=req.user)
    print(req.user.username)
    profile = Profile.objects.get(user_id=user.id)
    if req.method == 'POST':
        if req.POST.get('about'):
            print('收到ajax请求中about参数：', req.POST.get('about'))
            profile.bio = req.POST.get('about')
            profile.save()
            return HttpResponse('ok')
        elif req.FILES.get('avatar1'):
            print('收到ajax请求中头像：', req.FILES.get('avatar1'))
            profile.avatar = req.FILES.get('avatar1')
            profile.save()
            return HttpResponse('ok')
        profile_form = ProfileForm(data=req.POST)
        if profile_form.is_valid():
            profile_cd = profile_form.cleaned_data
            profile.phone = profile_cd['phone']
            profile.bio = profile_cd['bio']
            profile.save()
            return redirect('edit')
        else:
            return HttpResponse('输入错误')
    else:
        profile_form = ProfileForm
        context = {
            "profile_form": profile_form,
            "profile": profile,
            "user": user,
        }
        return render(req, 'userprofile/edit.html', context)


def sendsms(request):
    # smscode = random.randint(1000, 9999)
    phone = request.POST.get('phone')

    header_dict = {
        # "User-Agent": 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
        "X-Bmob-Application-Id": "edd7d7d21712e14c25372f9a43910965",
        "X-Bmob-REST-API-Key": "31f1f759a08678427bb09649fdd028ed",
        "Content-Type": "application/json"
    }

    body = {
        "mobilePhoneNumber": phone,
    }
    res = requests.post('https://api2.bmob.cn/1/requestSmsCode', data=body, headers=header_dict)
    res = res.json()

    # data = {
    #     "sid": "ef7af5bea30e52d62a6d5a05bad8b339",
    #     "token": "97e3b5c0bef705e7571434c961f6479d",
    #     "appid": "6a362ee8eaaa460bbe54a6b0710aea51",
    #     "templateid": 580742,
    #     "param": smscode,  # 上面生成的随机验证码
    #     "mobile": phone,  # 前端传过来的号码
    # }
    # 用云之讯第三方发短信
    res = requests.post('https://api2.bmob.cn/1/requestSmsCode', data=body, headers=header_dict)
    res = res.json()
    if res['code'] == '000000':

        # 保存验证码，保存在缓存里面，给一个过期时间
        # 实例化redis
        redis_cli = get_redis_connection()
        redis_cli.set(f'sms-{phone}', smscode, 60)
        return JsonResponse({'res': 'yes'})  # 发送验证码成功,证明手机号存在
    else:
        return JsonResponse({'res': 'no'})  # 发送验证码成功,证明手机号不存在


def test_redis(request):
    # 存储数据
    redis_cli = get_redis_connection()
    redis_cli.set('sms', 'sunnan', 60)
    # 判断Redis中是否存在
    print(redis_cli)  # 包含: true
    # 获取
    print(redis_cli.get("sms"))  # 返回: tom  无返回null
    return HttpResponse("测试Redis")
