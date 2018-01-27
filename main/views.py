from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator
from .models import Post, Tag
from datetime import datetime
import markdown


# 首页每一页的文章数量
INDEX_POST_PER_PAGE = 8
# 博客诞生年份
BLOG_START_YEAR = 2018


# 求两段时间相差的日数和小时数
def __get_phase_days_and_hours(now, old):
    years = now.year - old.year
    days = now.day - old.day
    hours = now.hour - old.hour

    # 日数基数
    days += years * 365
    # 往年闰年补差
    for i in range(old.year, now.year):
        if int(i % 100) == 0:
            if int(i % 400) == 0:
                days += 1
        else:
            if int(i % 4) == 0:
                days += 1
    # 今年闰年补差
    if now.month > 2:
        days += 1

    # 如果小时差为负数，则小时数+24，日数-1
    if hours < 0:
        hours += 24
        days -= 1

    # 返回字典
    return {
        'days': days,
        'hours': hours
    }


# 首页请求
def index(request):
    # 获取所有文章，按照时间顺序排序
    posts = Post.objects.all().order_by('-created_time')
    # 页数为 1
    page = 1
    # 获取总页数
    page_num = int(len(posts) / INDEX_POST_PER_PAGE + 1)
    # 错误检测
    if not 0 < page <= page_num:
        return Http404()
    # 分页器
    paginator = Paginator(posts, INDEX_POST_PER_PAGE)
    posts_this_page = paginator.page(page)
    # 判断是否为第一页或最后一页
    is_first_page = page == 1
    is_last_page = page == page_num
    # 文章排序
    posts_left = list()
    posts_right = list()
    for i in range(0, len(posts_this_page)):
        if i % 2 == 0:
            posts_left.append(posts_this_page[i])
        else:
            posts_right.append(posts_this_page[i])

    # 渲染
    return render(request, 'main/index.html', context={
        'title': '首页-Kindem的博客',
        'is_first_page': is_first_page,
        'is_last_page': is_last_page,
        'posts_left': posts_left,
        'posts_right': posts_right,
        'page': page,
        'pre_page': page - 1,
        'next_page': page + 1
    })


# 首页请求2
def index2(request, page):
    # 获取所有文章，按照时间顺序排序
    posts = Post.objects.all().order_by('-created_time')
    # 获取总页数
    page_num = int(len(posts) / INDEX_POST_PER_PAGE + 1)
    # 错误检测
    if not 0 < int(page) <= page_num:
        return Http404()
    # 分页器
    paginator = Paginator(posts, INDEX_POST_PER_PAGE)
    posts_this_page = paginator.page(int(page))
    # 判断是否为第一页或最后一页
    is_first_page = page == 1
    is_last_page = page == page_num
    # 文章排序
    posts_left = list()
    posts_right = list()
    for i in range(0, len(posts_this_page)):
        if i % 2 == 0:
            posts_left.append(posts_this_page[i])
        else:
            posts_right.append(posts_this_page[i])

    # 渲染
    return render(request, 'main/index.html', context={
        'title': '首页-Kindem的博客',
        'is_first_page': is_first_page,
        'is_last_page': is_last_page,
        'posts_left': posts_left,
        'posts_right': posts_right,
        'page': int(page),
        'pre_page': int(page) - 1,
        'next_page': int(page) + 1
    })


# 关于页面请求
def about(request):
    return render(request, 'main/about.html', context={
        'title': '关于Kindem-Kindem的博客'
    })


# 文章页面
def post(request, pk):
    # 获取对象
    p = get_object_or_404(Post, pk=pk)
    # 渲染 Markdown
    p.body = markdown.markdown(
        p.body,
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc'
        ]
    )

    # 求时间差
    phase_created = __get_phase_days_and_hours(datetime.utcnow(), p.created_time)
    phase_modified = __get_phase_days_and_hours(datetime.utcnow(), p.modified_time)

    return render(request, 'main/post.html', context={
        'title': p.title + '-Kindem的博客',
        'post': p,
        'phase_days_created': phase_created['days'],
        'phase_hours_created': phase_created['hours'],
        'phase_days_modified': phase_modified['days'],
        'phase_hours_modified': phase_modified['hours']
    })


# 归档页面
def archive(request):
    # 获取所有文章
    posts = Post.objects.all().order_by('-created_time')
    # 获取当前年份
    year_now = datetime.now().year

    # 按照年份分类的文章聊表
    posts_every_year = list()
    # 获取每一年里发表的文章
    for i in range(0, year_now + 1 - BLOG_START_YEAR):
        posts_every_year.append({})
        posts_every_year[i]['year'] = BLOG_START_YEAR + i
        posts_every_year[i]['posts'] = list()
        for p in posts.filter(created_time__year=BLOG_START_YEAR + i):
            posts_every_year[i]['posts'].append(p)

    return render(request, 'main/archive.html', context={
        'title': '归档-Kindem的博客',
        'posts_evert_year': posts_every_year
    })