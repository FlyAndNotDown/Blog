from django.conf.urls import url
from . import views
from django.contrib.sitemaps import Sitemap
from django.contrib.sitemaps.views import sitemap
from .models import Post
from datetime import datetime
from .feeds import AllPostRssFeed


# 定制的 Sitemap
class PostSitemap(Sitemap):
    changeFreq = 'daily'
    priority = 0.5

    def items(self):
        return Post.objects.all()

    def lastmod(self, obj):
        return obj.modified_time

    def location(self, obj):
        return "/post/" + str(obj.pk)


class MainSitemap(Sitemap):
    changeFreq = 'daily'
    priority = 0.5

    def items(self):
        return ['/', '/archive', '/about']

    def lastmod(self, obj):
        return datetime.now()

    def location(self, obj):
        return obj


# sitemap列表
sitemaps = {
    'main': MainSitemap,
    'post': PostSitemap
}


app_name = 'main'
urlpatterns = [
    # 首页
    url(r'^$', views.index, name='index'),
    # 首页
    url(r'^(?P<page>[1-9][0-9]*)$', views.index2, name='index2'),
    # 关于页面
    url(r'^about$', views.about, name='about'),
    # 文章页面
    url(r'^post/(?P<pk>[1-9][0-9]*)$', views.post, name='post'),
    # 归档页面
    url(r'^archive$', views.archive, name='archive'),
    # sitemap
    url(r'^sitemap.xml$', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    # robots.txt
    url(r'^robots.txt$', views.robots, name='robots'),
    # 通知页面
    url(r'^message$', views.message, name='message'),
    # github登录
    url(r'^login/github$', views.login_github, name='login_github'),
    # RSS
    url(r'^rss$', AllPostRssFeed(), name='rss'),
    # 注销
    url(r'^login/logout$', views.logout, name='logout')
]