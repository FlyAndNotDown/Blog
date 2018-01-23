from django.conf.urls import url
from . import views

urlpatterns = [
    # 首页
    url(r'^$', views.index, name='index'),
    # 关于页面
    url(r'^about$', views.about, name='about')
]