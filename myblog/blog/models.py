from django.db import models


# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=200)
    crate_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user'


class Lanmus(models.Model):
    name = models.CharField(max_length=150, null=True)
    alias = models.CharField(max_length=150, null=True)  # 别名
    fid = models.CharField(max_length=150, default='无')  # 父节点
    keywords = models.CharField(max_length=100, default='无')  # 关键字
    describe = models.TextField(null=True)  # 描述

    lanmu = models.ForeignKey('self', on_delete=models.CASCADE,null=True)
    num = models.IntegerField(default=0)

    class Meta:
        db_table = 'lanmus'


class Article(models.Model):
    title = models.CharField(max_length=200, unique=True)
    neirong = models.TextField()
    guanjianzi = models.CharField(max_length=200)
    miaoshu = models.CharField(max_length=200)
    lanmu = models.CharField(max_length=10, null=False)
    biaoqian = models.CharField(max_length=500)

    icon = models.ImageField(upload_to='upload', null=True)

    jiami = models.IntegerField(default=1, null=False)
    time = models.DateTimeField(auto_now_add=True)
    move = models.CharField(max_length=10, null=False)

    lanmus = models.ForeignKey(Lanmus, on_delete=models.CASCADE,null=True)

    class Meta:
        db_table = 'article'


class Yonghu(models.Model):
    name = models.CharField(max_length=10, unique=True, null=False)
    password = models.CharField(max_length=200, null=True)
    icon = models.ImageField(upload_to='upload', null=True)


    class Meta:
        db_table = 'yonghu'


# 首页相册
class Share(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False)
    icon = models.ImageField(upload_to='upload', null=True)
    content = models.TextField()

    class Meta:
        db_table = 'share'
