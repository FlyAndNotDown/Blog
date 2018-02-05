from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.paginator import Paginator
from .models import Post, KUser, Comment
from datetime import datetime
import urllib.parse
import urllib.request
import markdown
import json
import pytz


# 首页每一页的文章数量
INDEX_POST_PER_PAGE = 8
# 博客诞生年份
BLOG_START_YEAR = 2018

# GitHub登录API参数
github_client_id = '2b18fc8f7305f2e73416'
github_client_secret = 'eee6029f6f6f5873cc3fc8fcf9ebdb86ef375349'
# QQ 登录API参数
qq_client_id = '101456289'
qq_client_secret = 'b26af05256f42dce9c81e5fcc4db0195'

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
        'description': '专注技术的小博客，这里有你想学的技术，有众多干货分享-Kindem的博客',
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
        'description': '专注技术的小博客，这里有你想学的技术，有众多干货分享-Kindem的博客',
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
        'title': '关于Kindem-Kindem的博客',
        'description': 'Kindem:一只想做全栈开发者的野生程序猿-Kindem的博客'
    })


# 文章页面
def post(request, pk):
    # 获取对象
    p = get_object_or_404(Post, pk=pk)
    # 渲染 Markdown
    p.body = markdown.markdown(
        p.body,
        extensions=[
            'markdown.extensions.sane_lists',
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
            'markdown.extensions.abbr',
            'markdown.extensions.attr_list',
            'markdown.extensions.def_list',
            'markdown.extensions.fenced_code',
            'markdown.extensions.footnotes',
            'markdown.extensions.smart_strong',
            'markdown.extensions.meta',
            'markdown.extensions.nl2br',
            'markdown.extensions.tables'
        ]
    )

    # 求时间差
    phase_created = datetime.utcnow().replace(tzinfo=pytz.timezone('UTC')) - p.created_time
    phase_modified = datetime.utcnow().replace(tzinfo=pytz.timezone('UTC')) - p.modified_time

    # 保存登录之前的页面
    request.session['login_from'] = '/post/' + str(p.pk)

    # 获取一篇文章中的所有评论
    comments_all = Comment.objects.filter(post=p.pk)
    # 将所有用户的PK替换成实际的用户
    for comment in comments_all:
        comment.sender = KUser.objects.get(pk=comment.sender)
        comment.receiver = KUser.objects.get(pk=comment.receiver)
    # 取得这些评论中的所有父级评论
    comments_level_1 = comments_all.filter(level=1)
    # 新建一个list(dict())表用于存放所有的评论
    comments = list()
    i = 0
    # 遍历所有父级评论
    for parent in comments_level_1:
        comments.append(dict())
        # 为孩子评论预分配空间
        comments[i]['children'] = list()
        # 存入父级评论
        comments[i]['parent'] = parent
        # 存入孩子评论
        for child in comments_all.filter(level=2, parent=parent.pk):
            comments[i]['children'].append(child)
        # 迭代
        i += 1

    # 获取用户登录状态
    if request.session.get('login_state'):
        login_state = True
        user_type = request.session.get('user_type')
        uid = request.session.get('uid')
        nickname = request.session.get('nickname')
        avatar = request.session.get('avatar')
    else:
        login_state = False
        user_type = ''
        uid = ''
        nickname = ''
        avatar = ''

    return render(request, 'main/post.html', context={
        'title': p.title + '-Kindem的博客',
        'description': p.title + ':' + p.excerpt + '-Kindem的博客',
        'post': p,
        'login_state': login_state,
        'user_type': user_type,
        'uid': uid,
        'nickname': nickname,
        'avatar': avatar,
        'comments': comments,
        'comments_num': len(comments_all),
        'github_login_link': 'https://github.com/login/oauth/authorize?client_id=' + github_client_id,
        'qq_login_link': 'https://graph.qq.com/oauth2.0/authorize?response_type=code&' +
                        'client_id=' + qq_client_id + '&redirect_uri=http://www.kindemh.cn/login/qq',
        'phase_days_created': phase_created.days,
        'phase_hours_created': int(phase_created.seconds / 3600),
        'phase_days_modified': phase_modified.days,
        'phase_hours_modified': int(phase_modified.seconds / 3600)
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
        'description': '归档-Kindem的博客',
        'posts_evert_year': posts_every_year
    })


# robots.txt
def robots(request):
    return HttpResponse(r'User-agent: *\nAllow: /')


class MessageCard:
    """
    通知卡片类
    """
    def __init__(self, title, text, links):
        """
        构造
        :param title: 标题
        :param text: 内容
        :param links: 链接字典列表
        """
        self.title = title
        self.text = text
        self.links = list()
        for link in links:
            self.links.append(link)


# 通知页面
def message(request):
    # 左右两侧的通知卡片
    left_cards = list()
    right_cards = list()
    # 如果用户已经登录了
    if request.session.get('login_state'):
        return render(request, 'main/message.html', context={
            'title': '通知-Kindem的博客',
            'description': '通知-Kindem的博客',
            'left_cards': left_cards,
            'right_cards': right_cards
        })

    else:
        # 保存登录之前的页面
        request.session['login_from'] = '/message'

        left_cards.append(MessageCard(
            '你还没登录哦!',
            '使用下面给出的第三方认证登录本站来参与评论', [{
                'name': 'GitHub',
                'href': 'https://github.com/login/oauth/authorize?client_id=' + github_client_id
            }, {
                'name': 'QQ',
                'href': 'https://graph.qq.com/oauth2.0/authorize?response_type=code&' +
                        'client_id=' + qq_client_id + '&redirect_uri=http://www.kindemh.cn/login/qq'
            }]
        ))
        return render(request, 'main/message.html', context={
            'title': '通知-Kindem的博客',
            'description': '通知-Kindem的博客',
            'left_cards': left_cards,
            'right_cards': right_cards
        })


# github登录回调
def login_github(request):
    # 获取 code
    code = request.GET.get('code')
    # 准备POST参数用于交换 access_token
    data = bytes(urllib.parse.urlencode({
        'client_id': github_client_id,
        'client_secret': github_client_secret,
        'code': code
    }), encoding='utf8')
    # 发送Http请求用于交换 access_token
    response = urllib.request.urlopen('https://github.com/login/oauth/access_token', data=data)
    # 提取 access_token
    access_token = str(response.read(), encoding='utf-8').split('&')[0].split('=')[1]
    # 使用 access_token 获取用户信息
    response = urllib.request.urlopen('https://api.github.com/user?access_token=' + access_token)
    # 解码成Python对象
    user_info = json.loads(response.read().decode('utf-8'))
    user_info['id'] = str(user_info['id'])

    # 查询数据库，看用户是否已经在数据库中
    # 如果已经有了
    if KUser.objects.filter(user_type='github', uid=user_info['id']).exists():
        # 将登陆信息存入 session
        request.session['login_state'] = True
        request.session['user_type'] = 'github'
        request.session['uid'] = user_info['id']
        request.session['nickname'] = user_info['login']
        request.session['avatar'] = user_info['avatar_url']
    # 如果没有
    else:
        # 将信息存入 session 和数据库
        request.session['login_state'] = True
        request.session['user_type'] = 'github'
        request.session['uid'] = user_info['id']
        request.session['nickname'] = user_info['login']
        request.session['avatar'] = user_info['avatar_url']
        k_user = KUser(
            user_type='github',
            uid=user_info['id'],
            nickname=user_info['login'],
            avatar=user_info['avatar_url'])
        k_user.save()

    # 返回，并且重定向到登录前的网站
    return HttpResponseRedirect(request.session['login_from'])


# qq登录回调
def login_qq(request):
    # 获取 code
    code = request.GET.get('code')
    # 通过 code 获取Access Token
    response = urllib.request.urlopen(
        'https://graph.qq.com/oauth2.0/token?' +
            'grant_type=authorization_code' +
            '&client_id=' + qq_client_id +
            '&client-secret=' + qq_client_secret +
            '&code=' + code +
            '&redirect_uri=' + 'http://www.kindemh.cn/login/qq')
    # 提取 access_token
    access_token = response.read().decode('utf-8').split('&')[0].split('=')[1]
    return HttpResponse(response)
    # # 使用 access_token 获取用户的 openid
    # response = urllib.request.urlopen(
    #     'https://graph.qq.com/oauth2.0/me?' +
    #         'access_token=' + access_token
    # )
    # # 解码成Python对象
    # json_obj = json.loads(response.read().decode('utf-8'))
    # openid = json_obj['openid']
    # # 使用 openid 用户的信息
    # response = urllib.request.urlopen(
    #     'https://graph.qq.com/user/get_user_info?' +
    #         'access_token=' + access_token +
    #         '&oauth_consumer_key=' + qq_client_id +
    #         '&openid=' + openid)
    # # 解析成Python对象
    # user_info = json.loads(response.read().decode('utf-8'))
    #
    # # 查询数据库，看用户是否已经在数据库之中了
    # # 如果已经有了
    # if KUser.objects.filter(user_type='qq', uid=openid).exists():
    #     # 将登录信息存入 session
    #     request.session['login_state'] = True
    #     request.session['user_type'] = 'qq'
    #     request.session['uid'] = openid
    #     request.session['nickname'] = user_info['nickname']
    #     request.session['avatar'] = user_info['figureurl_qq_1']
    # # 如果有没
    # else:
    #     # 将信息存入 session 和数据库
    #     request.session['login_state'] = True
    #     request.session['user_type'] = 'qq'
    #     request.session['uid'] = openid
    #     request.session['nickname'] = user_info['nickname']
    #     request.session['avatar'] = user_info['figureurl_qq_1']
    #     k_user = KUser(
    #         user_type='qq',
    #         uid=openid,
    #         nickname=user_info['nickname'],
    #         avatar=user_info['figureurl_qq_1'])
    #     k_user.save()


# 注销
def logout(request):
    request.session['login_state'] = False
    request.session['user_type'] = None
    request.session['uid'] = None
    request.session['nickname'] = None
    request.session['avatar'] = None
    return HttpResponse(json.dumps({
        'state': True
    }))