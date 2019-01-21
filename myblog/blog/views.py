from django.contrib.auth.hashers import check_password, make_password
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms

# Create your views here.
from django.urls import reverse

from blog.models import User, Article, Lanmus, Yonghu


# (登陆注册)=====================================================================================


def index(request):
    # 获取数据
    if request.method == 'GET':
        article = Article.objects.all()
        num = len(article)
        lan = Lanmus.objects.all()
        for la in lan:

            num1 = Article.objects.filter(lanmus=la.id)
            num11 = len(num1)
            la.num = num11
            la.save()
        return render(request, 'index.html', {'article': article, 'lan': lan, 'num':num})


def loding(request):
    if request.method == 'GET':
        loding = 'Loding . . .'
        return render(request, 'article.html', {'loding': loding})


# 登录
def my_login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('userpwd')
        user = User.objects.filter(username=username).first()
        if check_password(password, user.password):

            request.session['user_id'] = user.id
            return HttpResponseRedirect(reverse('blog:article'))

        else:
            msg = '账号或密码错误'
            return render(request, 'login.html', {'msg': msg})



# 退出登录 最好用session
def loginout(request):
    if request.method == 'GET':
        # 跳转到登录页面
        out = HttpResponseRedirect(reverse('blog:my_login'))
        # 删除token中的信息
        out.delete_cookie('token')
        return out


# 注册
def register(request):
    if request.method == 'GET':
        return render(request, 'registerl.html')
    if request.method == 'POST':
        # 1. 接收页面中传递的参数
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        # 2. 实现保存用户信息到user表中
        if User.objects.filter(username=username).exists():
            msg = '账号已存在'
            return render(request, 'registerl.html', {'msg': msg})
        if password != password2:
            msg = '密码不一致'
            return render(request, 'registerl.html', {'msg': msg})
        password = make_password(password)
        User.objects.create(username=username, password=password)
        # 登陆跳转
        return HttpResponseRedirect(reverse('blog:my_login'))


# 文章分页
def article(request):
    if request.method == 'GET':
        page = int(request.GET.get('page', 1))
        article = Article.objects.all()
        numm = len(article)
        pg = Paginator(article, 6)
        article = pg.page(page)
        return render(request, 'article.html', {'article': article, 'numm':numm})


# 文章添加
def add_article(request):
    if request.method == 'GET':
        lanmus = Lanmus.objects.all()
        return render(request, 'add-article.html', {'lanmus': lanmus})

    if request.method == 'POST':

        # 1、获取数据
        title = request.POST.get('title')
        neirong = request.POST.get('content')
        guanjianzi = request.POST.get('keywords')
        miaoshu = request.POST.get('describe')
        lanmu = request.POST.get('category')
        biaoqian = request.POST.get('tags')
        icon = request.FILES.get('titlepic')  # 标题图片
        jiami = request.POST.get('visibility')  # 加密
        # time = request.POST.get('time')          # 发布时间
        # move = request.POST.get('submit')        # 更新时间

        article = Article.objects.all()
        for art in article:
            if title == art.title:
                ti = '不能重名. . .'
                return render(request, 'add-article.html', {'ti': ti})
        else:
            # 2、保存到数据库
            Article.objects.create(title=title, neirong=neirong, guanjianzi=guanjianzi, miaoshu=miaoshu,
                                   lanmu=lanmu, biaoqian=biaoqian, icon=icon, jiami=jiami, lanmus_id=lanmu)
            # 3、跳转到列表页面
            return render(request, 'article.html', {'article': article})
    else:
        c = '添加失败，请继续...'
        return render(request, 'add-article.html', {'c': c})


# 删除文章
def article_delete(request, id):
    if request.method == 'GET':
        Article.objects.filter(id=id).delete()
        return HttpResponseRedirect(reverse('blog:article'))


# 修改文章
def article_update(request, id):
    if request.method == 'GET':
        article = Article.objects.filter(pk=id).first()

        return render(request, 'update-article.html', {'title': article.title, 'neirong': article.neirong,
                                                       'guanjianzi': article.guanjianzi, 'miaoshu': article.miaoshu,
                                                       'biaoqian': article.biaoqian})
    if request.method == 'POST':
        article = Article.objects.filter(pk=id).first()
        if article.icon:
            article.icon.flush()
        title = request.POST.get('title')
        neirong = request.POST.get('content')
        guanjianzi = request.POST.get('keywords')
        miaoshu = request.POST.get('describe')
        lanmu = request.POST.get('category')
        biaoqian = request.POST.get('tags')  # 标签
        icon = request.FILES.get('titlepic')  # 标题图片
        jiami = request.POST.get('visibility')  # 加密

        # 2、保存到数据库

        article.title = str(title)
        article.neirong = str(neirong)
        article.guanjianzi = str(guanjianzi)
        article.miaoshu= str(miaoshu)
        article.lanmu = lanmu
        article.biaoqian = str(biaoqian)
        article.icon = icon
        article.jiami = jiami
        article.save()
        # 3、跳转到列表页面
        return HttpResponseRedirect(reverse('blog:article'))  # render(request, 'article.html', {'article': article})
    else:
        u = '修改失败，请继续...'
        return render(request, 'update-article.html', {'u': u})


# 栏目添加
def category(request):
    if request.method == 'GET':
        lanmu = Lanmus.objects.all()
        return render(request, 'category.html', {'lanmu': lanmu})
    if request.method == 'POST':
        name = request.POST.get('name')
        alias = request.POST.get('alias')
        fid = request.POST.get('fid')
        keywords = request.POST.get('keywords')
        describe = request.POST.get('describe')
        Lanmus.objects.create(name=name, alias=alias, fid=fid, keywords=keywords, describe=describe)

        lanmu = Lanmus.objects.all()

        return render(request, 'category.html', {'lanmu': lanmu})


# 栏目删除
def del_category(request, id):
    if request.method == 'GET':
        Lanmus.objects.filter(pk=id).delete()
        return HttpResponseRedirect(reverse('blog:category'))


# 栏目修改
def upd_category(request, id):
    if request.method == 'GET':
        ziduan = Lanmus.objects.filter(pk=id).first()
        return render(request, 'update-category.html',
                      {'name': ziduan.name, 'alias': ziduan.alias, 'fid': ziduan.fid, 'keywords': ziduan.keywords,
                       'describe': ziduan.describe})
    # 获取数据，并添加到数据库
    if request.method == 'POST':
        name = request.POST.get('name')
        alias = request.POST.get('alias')
        fid = request.POST.get('fid')
        keywords = request.POST.get('keywords')
        describe = request.POST.get('describe')
        Lanmus.objects.filter(pk=id).update(name=name, alias=alias, fid=fid, keywords=keywords, describe=describe)

        return HttpResponseRedirect(reverse('blog:category'))


# 用户登录
def yh_login(request):
    if request.method == 'GET':
        return render(request, 'yh_login.html')
    if request.method == 'POST':
        name = request.POST.get('yusername')
        password = request.POST.get('yuserpwd')
        yonghu = Yonghu.objects.filter(name=name).first()
        if not yonghu:
            msg = '没有此账号 . . .'
            return render(request, 'yh_login.html', {'msg': msg})

        if check_password(password, yonghu.password):

            request.session['user_id'] = yonghu.id
            return HttpResponseRedirect(reverse('blog:index'))

        else:
            msg = '账号或密码错误 . . .'
            return render(request, 'yh_login.html', {'msg': msg})


# 用户注册
def yh_register(request):
    if request.method == 'GET':
        return render(request, 'yh_register.html')
    if request.method == 'POST':
        # 1. 接收页面中传递的参数
        name = request.POST.get('yusername')
        password = request.POST.get('ypassword')
        password2 = request.POST.get('ypassword2')
        # 2. 实现保存用户信息到user表中
        if Yonghu.objects.filter(name=name).exists():
            msg = '账号已存在 . . .'
            return render(request, 'yh_register.html', {'msg': msg})
        if password != password2:
            msg = '密码不一致 . . .'
            return render(request, 'yh_register.html', {'msg': msg})
        password = make_password(password)
        Yonghu.objects.create(name=name, password=password)
        # 登陆跳转
        return HttpResponseRedirect(reverse('blog:yh_login'))


# 主页渲染
def info(request, id):
    if request.method == 'GET':
        info_id = Article.objects.filter(pk=id).first()
        yh = Yonghu.objects.all()
        y = yh.count()

        lan = Lanmus.objects.all()

        return render(request, 'info.html', {'info_id': info_id, 'y': y, 'lan': lan})


def infopic(request):
    if request.method == 'GET':
        lan = Lanmus.objects.all()
        return render(request, 'infopic.html', {'lan': lan})




def indexl(request,id):
    if request.method == 'GET':
        jihe = Lanmus.objects.filter(pk=id).first()
        ji = jihe.article_set.all()
        article = Article.objects.all()
        lan = Lanmus.objects.all()
        for la in lan:
            num1 = Article.objects.filter(lanmus=la.id)
            num11 = len(num1)
            la.num = num11
            la.save()
        return render(request, 'index1.html', {'ji':ji, 'lan': lan})

def riji(request):
    # 获取数据
    if request.method == 'GET':
        page = int(request.GET.get('page', 1))
        article = Article.objects.all()
        pg = Paginator(article, 6)
        article = pg.page(page)
        lan = Lanmus.objects.all()
        for la in lan:

            num1 = Article.objects.filter(lanmus=la.id)
            num11 = len(num1)
            la.num = num11
            la.save()
        return render(request, 'riji.html', {'article': article, 'lan': lan})


def about(request):
    # 获取数据
    if request.method == 'GET':
        lan = Lanmus.objects.all()
        for la in lan:
            num1 = Article.objects.filter(lanmus=la.id)
            num11 = len(num1)
            la.num = num11
            la.save()
        return render(request, 'about.html', {'lan': lan})

