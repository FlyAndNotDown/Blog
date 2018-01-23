from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator
from .models import Post, Tag


# 首页每一页的文章数量
INDEX_POST_PER_PAGE = 4


def index(request):
    # 获取所有文章，按照时间顺序排序
    posts = Post.objects.all().order_by('-created_time')
    # 页数为 1
    page = 1
    # 获取总页数
    page_num = len(posts) / INDEX_POST_PER_PAGE + 1
    # 错误检测
    if not 0 < page <= page_num:
        return Http404()
    # 分页器
    paginator = Paginator(posts, INDEX_POST_PER_PAGE)
    posts_this_page = paginator.page(page)
    # 判断是否为第一页或最后一页
    is_first_page = page == 1
    is_last_page = page == page_num

    # 渲染
    return render(request, 'main/index.html', context={
        'title': '首页-Kindem的博客',
        'is_first_page': is_first_page,
        'is_last_page': is_last_page,
        'posts1': posts_this_page[0:2],
        'posts2': posts_this_page[2:],
        'page': page,
        'pre_page': page - 1,
        'next_page': page + 1
    })


def index2(request, page):
    # 获取所有文章，按照时间顺序排序
    posts = Post.objects.all().order_by('-created_time')
    # 获取总页数
    page_num = len(posts) / INDEX_POST_PER_PAGE + 1
    # 错误检测
    if not 0 < int(page) <= page_num:
        return Http404()
    # 分页器
    paginator = Paginator(posts, INDEX_POST_PER_PAGE)
    posts_this_page = paginator.page(int(page))
    # 判断是否为第一页或最后一页
    is_first_page = page == 1
    is_last_page = page == page_num

    # 渲染
    return render(request, 'main/index.html', context={
        'title': '首页-Kindem的博客',
        'is_first_page': is_first_page,
        'is_last_page': is_last_page,
        'posts1': posts_this_page[0:2],
        'posts2': posts_this_page[2:],
        'page': int(page),
        'pre_page': int(page) - 1,
        'next_page': int(page) + 1
    })


def about(request):
    return render(request, 'main/about.html', context={
        'title': '关于Kindem-Kindem的博客'
    })


def post(request, pk):
    p = get_object_or_404(Post, pk=pk)
    return render(request, 'main/post.html', context={
        'post': p
    })
