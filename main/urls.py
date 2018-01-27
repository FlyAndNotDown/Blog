from django.conf.urls import url
from . import views


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
    url(r'^archive$', views.archive, name='archive')
]