# Paul7Sk8 Blog 孙楠个人网站
python3.7 Django2.2

## Description 描述
个人技术经验网站，有基本的文章评论、用户注册、统计浏览量、站内消息功能。

该网站未来设计蓝图：
+ 结合浏览器插件，方便快捷的抓取文章到本网站记录文库。
+ 记录自己的浏览，使用艾宾浩斯记忆曲线规律每天推送需要强化记忆的重点内容。
+ 申请微信公众号/服务号每天强制推送至微信。


## Install 安装步骤

1. 安装虚拟环境，python版本选择3.7
2. pip安装依赖包```pip install -r requirements.txt```
3. 把自己的mysql、redis参数在setting文件中配置好
4. 数据库表创建 ```python manage.py makemigrations``` ```python manage.py migrate```

## Demo演示

[网站Demo演示链接](http://43.226.69.84)

