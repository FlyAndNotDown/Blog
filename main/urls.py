from django.conf.urls import url
from . import views
from django.contrib.sitemaps.views import sitemap
from main.tool.feeds import AllPostRssFeed
from main.tool.sitemap import MainSitemap, PostSitemap


# sitemap列表
sitemaps = {
    'main': MainSitemap,
    'post': PostSitemap
}


app_name = 'main'
urlpatterns = [
    # 首页
    url(r'^$', views.index__normal, name='index__normal'),
    # 首页
    url(r'^(?P<page>[1-9][0-9]*)$', views.index__param, name='index__param'),

    # 关于页面
    url(r'^about$', views.about, name='about'),

    # 通知页面
    url(r'^message$', views.message, name='message'),

    # 文章页面
    url(r'^post/(?P<pk>[1-9][0-9]*)$', views.post, name='post'),

    # 归档页面
    url(r'^archive$', views.archive, name='archive'),

    # sitemap
    url(r'^sitemap.xml$', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    # robots.txt
    url(r'^robots.txt$', views.robots, name='robots'),
    # RSS
    url(r'^rss$', AllPostRssFeed(), name='rss'),

    # 登录请求
    # 本站注册请求
    url(r'^login/register/local$', views.login_register_local, name='login_register_local')
]