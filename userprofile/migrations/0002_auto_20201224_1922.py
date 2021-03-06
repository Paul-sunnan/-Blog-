# Generated by Django 2.2 on 2020-12-24 11:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailVeriRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, verbose_name='验证码')),
                ('email', models.EmailField(max_length=50, verbose_name='用户邮箱')),
                ('send_time', models.DateTimeField(blank=True, default=datetime.datetime.now, null=True, verbose_name='发送时间')),
                ('exprie_time', models.DateTimeField(null=True)),
                ('email_type', models.CharField(choices=[('register', '注册邮件'), ('forget', '找回密码')], max_length=10)),
            ],
            options={
                'verbose_name': '邮件验证码',
                'verbose_name_plural': '邮件验证码',
            },
        ),
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='avatar/%Y%m%d'),
        ),
    ]
