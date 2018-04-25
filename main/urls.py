from django.conf.urls import url
from main import views
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
    url(r'^login/local/register$', views.login_local_register, name='login_local_register'),
    # 本站登录-获取盐
    url(r'^login/local/get_salt$', views.login_local_get_salt, name='login_local_get_salt'),
    # 本站登录
    url(r'^login/local/login$', views.login_local_login, name='login_local_login'),
    # 本站管理员登录
    url(r'^login/local/admin_login', views.login_local_admin__login, name='login_local_admin__login'),
    # 注销请求
    url(r'^login/logout$', views.login_logout, name='login_logout'),
    # GitHub登录回调
    url(r'^login/github/callback$', views.login_github_callback, name='login_github_callback'),
    # QQ 登录回调
    url(r'^login/qq/callback$', views.login_qq_callback, name='login_qq_callback'),

    # 评论系统
    # 发表评论
    url(r'^comment/publish$', views.comment_publish, name='comment_publish'),
    # 发表回复
    url(r'^comment/reply$', views.comment_reply, name='comment_reply'),

    # 管理员系统
    # 管理员主页
    url(r'^kadmin$', views.kadmin, name='kadmin'),
    # 文件管理页面
    url(r'^kadmin/file$', views.kadmin_file, name='kadmin_file'),

    # 图片管理系统
    # 图片上传
    url(r'^picture/upload$', views.picture_upload, name='file_upload')
]