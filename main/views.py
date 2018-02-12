from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from main.models import KUser

from .view.index import *
from .view.login import *
from .view.header import *
from .view.archive import *
from .view.about import *
from .view.post import *
from .view.comment import *

import json


# ----------------------------------------------------- # check
# 首页请求
def index__normal(request):
    index_render = IndexRender(1)
    return render(request, 'main/index.html', context={
        'header': Header(
            title='首页_IT小站_专注技术的小博客',
            description='IT小站，专注技术的小博客，这里有你想学的技术，有众多干货分享。',
            keywords='it,it小站'
        ),
        'page_info': index_render.get_page_info(),
        'post_list': index_render.get_post_list(),
        'slogan_box': IndexSloganBox()
    })


# 首页请求2
def index__param(request, page):
    index_render = IndexRender(page)
    return render(request, 'main/index.html', context={
        'header': Header(
            title='首页_IT小站_专注技术的小博客',
            description='IT小站，专注技术的小博客，这里有你想学的技术，有众多干货分享。',
            keywords='it,it小站'
        ),
        'page_info': index_render.get_page_info(),
        'post_list': index_render.get_post_list(),
        'slogan_box': IndexSloganBox()
    })


# ----------------------------------------------------- # check
# 归档页面
def archive(request):
    archive_render = ArchiveRender()
    return render(request, 'main/archive.html', context={
        'header': Header(
            title='首页_IT小站_专注技术的小博客',
            keywords='it,it小站',
            description='IT小站，专注技术的小博客，这里有你想学的技术，有众多干货分享。'
        ),
        'posts_evert_year': archive_render.get_posts_every_year(),
        'slogan_box': ArchiveSloganBox()
    })


# ----------------------------------------------------- # check
# 关于页面请求
def about(request):
    return render(request, 'main/about.html', context={
        'header': Header(
            title='首页_IT小站_专注技术的小博客',
            keywords='it,it小站',
            description='IT小站，专注技术的小博客，这里有你想学的技术，有众多干货分享。'
        ),
        'slogan_box': AboutSloganBox(),
        'introduction_box': AboutIntroductionBox(),
        'experience_box': AboutExperienceBox(),
        'skill_box': AboutSkillBox()
    })


# ----------------------------------------------------- #
# 文章页面
def post(request, pk):
    # 储存登录前的位置
    request.session['login_from'] = '/post/' + str(pk)

    # 获取登录信息
    login_state = request.session.get('login_state', False)
    user_info = None
    if login_state:
        user_info = request.session.get('user_info', None)

    # 进行渲染
    post_render = PostRender(pk, login_state, user_info)

    if post_render.error_happen():
        return Http404()
    else:
        return render(request, 'main/post.html', context={
            'header': Header(
                title=post_render.get_post().title + '_IT小站_专注技术的小博客',
                description=post_render.get_post().excerpt,
                keywords=post_render.get_post().keywords
            ),
            'post': post_render.get_post(),
            'phase_time': post_render.get_phase_time(),
            'login_info': post_render.get_login_info(),
            'login_param': {
                'github': github_param,
                'qq': qq_param
            },
            'comments_info': {
                'comments': post_render.get_comments(),
                'length': post_render.get_comments_length()
            }
        })


# ----------------------------------------------------- #
# 登录请求
# 本站注册请求
@csrf_exempt
def login_local_register(request):
    # 获取 json 数据
    jsonObj = json.loads(request.body.decode('utf-8'))
    username = jsonObj['username']
    password = jsonObj['password']
    salt = jsonObj['salt']

    # 处理请求
    login_register_local_request = LoginLocalRegisterRequest(
        username, password, salt
    )
    # 如果注册成功
    if login_register_local_request.get_response()['state']:
        # 在 session 中保存信息
        request.session['login_state'] = True
        request.session['user_info'] = login_register_local_request.get_user_info()
    # 返回 json 数据
    return HttpResponse(json.dumps(login_register_local_request.get_response()))


# 本站登录-获取 salt 请求
@csrf_exempt
def login_local_get_salt(request):
    # 获取 username
    jsonObj = json.loads(request.body.decode('utf-8'))
    username = jsonObj['username']

    # 处理请求
    login_local_get_salt_request = LoginLocalGetSaltRequest(username)
    return HttpResponse(json.dumps(login_local_get_salt_request.get_response()))


# 本站登录-登录验证请求
@csrf_exempt
def login_local_login(request):
    # 解析 json 字符串
    jsonObj = json.loads(request.body.decode('utf-8'))
    username = jsonObj['username']
    password = jsonObj['password']

    # 处理请求
    login_local_login_request = LoginLocalLoginRequest(
        username, password
    )
    # 如果成功登录了，就将用户信息存入 session
    if login_local_login_request.get_response()['state']:
        request.session['login_state'] = True
        request.session['user_info'] = login_local_login_request.get_user_info()
    # 返回 json 数据
    return HttpResponse(json.dumps(login_local_login_request.get_response()))


# 注销请求
def login_logout(request):
    # 清除 session 信息
    request.session['login_state'] = False
    request.session['user_info'] = None
    # 返回 json 数据
    return HttpResponse(json.dumps({'state': True}))


# GitHub 登录回调
def login_github_callback(request):
    # 获取 code
    code = request.GET.get('code')
    if code:
        # 执行请求
        login_github_callback_request = LoginGitHubCallbackRequest(code)
        # 如果登录成功了，就将用户信息存入 session
        if login_github_callback_request.get_response()['success']:
            request.session['login_state'] = True
            request.session['user_info'] = login_github_callback_request.get_response()['user_info']

    # 返回，并且重定向到登录前的 url
    return HttpResponseRedirect(request.session['login_from'])


# QQ 登录回调
def login_qq_callback(request):
    # 获取 code
    code = request.GET.get('code')
    if code:
        # 执行请求
        login_qq_callback_request = LoginQQCallbackRequest(code)
        # 如果登录成功了，就将用户信息存入 session
        if login_qq_callback_request.get_response()['success']:
            request.session['login_state'] = True
            request.session['user_info'] = login_qq_callback_request.get_response()['user_info']

    # 返回，并且重定向到登录前的 url
    return HttpResponseRedirect(request.session['login_from'])


# ----------------------------------------------------- #
# 评论系统
# 发表评论
@csrf_exempt
def comment_publish(request):
    # 解析 json 字符串
    jsonObj = json.loads(request.body.decode('utf-8'))
    sender_pk = jsonObj['sender']
    post_pk = jsonObj['post']
    context = jsonObj['context']
    # 执行请求
    comment_publish_request = CommentPublishRequest(
        sender=sender_pk,
        post=post_pk,
        context=context
    )
    # 返回数据
    return HttpResponse(json.dumps({'state': True}))


# ----------------------------------------------------- #
# robots.txt
def robots(request):
    return HttpResponse(r'User-agent: *\nAllow: /')


# ----------------------------------------------------- #
# 通知页面
def message(request):
    pass
    # # 左右两侧的通知卡片
    # left_cards = list()
    # right_cards = list()
    # # 如果用户已经登录了
    # if request.session.get('login_state'):
    #
    #     return render(request, 'main/message.html', context={
    #         'header': Header(
    #             title='首页_IT小站_专注技术的小博客',
    #             keywords='it,it小站,通知',
    #             description='IT小站，专注技术的小博客，这里有你想学的技术，有众多干货分享。'
    #         ),
    #         'left_cards': left_cards,
    #         'right_cards': right_cards
    #     })
    #
    # else:
    #     # 保存登录之前的页面
    #     request.session['login_from'] = '/message'
    #
    #     left_cards.append(MessageCard(
    #         '你还没登录哦!',
    #         '使用下面给出的第三方认证登录本站来参与评论', [{
    #             'name': 'GitHub',
    #             'href': 'https://github.com/login/oauth/authorize?client_id=' + github_client_id
    #         }, {
    #             'name': 'QQ',
    #             'href': 'https://graph.qq.com/oauth2.0/authorize?response_type=code&' +
    #                     'client_id=' + qq_client_id + '&redirect_uri=http://www.kindemh.cn/login/qq'
    #         }]
    #     ))
    #     return render(request, 'main/message.html', context={
    #         'header': Header(
    #             title='首页_IT小站_专注技术的小博客',
    #             keywords='it,it小站,通知',
    #             description='IT小站，专注技术的小博客，这里有你想学的技术，有众多干货分享。'
    #         ),
    #         'left_cards': left_cards,
    #         'right_cards': right_cards
    #     })
