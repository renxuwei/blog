from django.urls import path, re_path

from blog import views

urlpatterns = [
    # 127.0.0.1:8080/app/index/
    # re_path正则访问地址
    path('index/', views.index, name='index'),
    path('loding/', views.loding, name='loding'),
    # 或者path('index/<int:id>', views.index),
    path('my_login/', views.my_login, name='my_login'),
    path('register/', views.register, name='register'),
    path('loginout/', views.loginout, name='loginout'),

    path('article/', views.article, name='article'),

    path('add_article/', views.add_article, name='add_article'),
    path('article_delete/<int:id>/', views.article_delete, name='article_delete'),
    path('article_update/<int:id>/', views.article_update, name='article_update'),



    # 栏目
    path('category/', views.category, name='category'),
    path('del_category/<int:id>/', views.del_category, name='del_category'),
    path('upd_category/<int:id>/', views.upd_category, name='upd_category'),


    # 用户登录注册
    path('yh_login/', views.yh_login, name='yh_login'),
    path('yh_register/', views.yh_register, name='yh_register'),

    # 主页
    path('info/<int:id>/', views.info, name='info'),
    # path('infos/<int:id>/', views.infos, name='infos'),
    #path('infox/<int:id>/', views.infos, name='infos'),


    # path('share/', views.share, name='share'),
    path('indexl/<int:id>', views.indexl, name='indexl'),
    path('infopic/', views.infopic, name='infopic'),
    path('riji/', views.riji, name='riji'),
    path('about/', views.about, name='about'),



]