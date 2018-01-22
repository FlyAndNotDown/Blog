from django.shortcuts import render
from django.http import HttpResponse
from .models import Post, Tag


# Create your views here.
def index(request):
    # 获取所有文章，按照时间顺序排序
    posts = Post.objects.all().order_by('-created_time')
    return render(request, 'main/index.html', context={
        'posts': posts
    })
