from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect

from .view.index import *
from .view.login import *
from .view.header import *
from .view.archive import *
from .view.about import *
from .view.post import *


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
    post_render = PostRender(pk)
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
            'phase_time': post_render.get_phase_time()
        })

# def post(request, pk):
#     # 获取对象
#     p = get_object_or_404(Post, pk=pk)
#     # 渲染 Markdown
#     p.body = markdown.markdown(
#         p.body,
#         extensions=[
#             'markdown.extensions.sane_lists',
#             'markdown.extensions.extra',
#             'markdown.extensions.codehilite',
#             'markdown.extensions.toc',
#             'markdown.extensions.abbr',
#             'markdown.extensions.attr_list',
#             'markdown.extensions.def_list',
#             'markdown.extensions.fenced_code',
#             'markdown.extensions.footnotes',
#             'markdown.extensions.smart_strong',
#             'markdown.extensions.meta',
#             'markdown.extensions.nl2br',
#             'markdown.extensions.tables'
#         ]
#     )
#
#     # 求时间差
#     phase_created = datetime.utcnow().replace(tzinfo=pytz.timezone('UTC')) - p.created_time
#     phase_modified = datetime.utcnow().replace(tzinfo=pytz.timezone('UTC')) - p.modified_time
#
#     # 保存登录之前的页面
#     request.session['login_from'] = '/post/' + str(p.pk)
#
#     # 获取一篇文章中的所有评论
#     comments_all = Comment.objects.filter(post=p.pk)
#     # 将所有用户的PK替换成实际的用户
#     for comment in comments_all:
#         if comment.sender:
#             comment.sender = KUser.objects.get(pk=comment.sender)
#         if comment.receiver:
#             comment.receiver = KUser.objects.get(pk=comment.receiver)
#     # 取得这些评论中的所有父级评论
#     comments_level_1 = comments_all.filter(level=1)
#     # 新建一个list(dict())表用于存放所有的评论
#     comments = list()
#     i = 0
#     # 遍历所有父级评论
#     for parent in comments_level_1:
#         comments.append(dict())
#         # 为孩子评论预分配空间
#         comments[i]['children'] = list()
#         # 存入父级评论
#         comments[i]['parent'] = parent
#         # 存入孩子评论
#         for child in comments_all.filter(level=2, parent=parent.pk):
#             comments[i]['children'].append(child)
#         # 迭代
#         i += 1
#
#     # 获取用户登录状态
#     if request.session.get('login_state'):
#         login_state = True
#         user_type = request.session.get('user_type')
#         uid = request.session.get('uid')
#         nickname = request.session.get('nickname')
#         avatar = request.session.get('avatar')
#     else:
#         login_state = False
#         user_type = ''
#         uid = ''
#         nickname = ''
#         avatar = ''
#
#     return render(request, 'main/post.html', context={
#         'header': Header(
#             title=p.title + '_IT小站_专注技术的小博客',
#             description=p.excerpt,
#             keywords=p.keywords
#         ),
#         'post': p,
#         'login_state': login_state,
#         'user_type': user_type,
#         'uid': uid,
#         'user_pk': KUser.objects.get(user_type=user_type, uid=uid).pk,
#         'nickname': nickname,
#         'avatar': avatar,
#         'comments': comments,
#         'comments_num': len(comments_all),
#         'github_login_link': 'https://github.com/login/oauth/authorize?client_id=' + github_client_id,
#         'qq_login_link': 'https://graph.qq.com/oauth2.0/authorize?response_type=code&' +
#                         'client_id=' + qq_client_id + '&redirect_uri=http://www.kindemh.cn/login/qq',
#         'phase_days_created': phase_created.days,
#         'phase_hours_created': int(phase_created.seconds / 3600),
#         'phase_days_modified': phase_modified.days,
#         'phase_hours_modified': int(phase_modified.seconds / 3600)
#     })


# ----------------------------------------------------- #
# robots.txt
def robots(request):
    return HttpResponse(r'User-agent: *\nAllow: /')


# ----------------------------------------------------- #
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


# ----------------------------------------------------- #
# 通知页面
def message(request):
    # 左右两侧的通知卡片
    left_cards = list()
    right_cards = list()
    # 如果用户已经登录了
    if request.session.get('login_state'):

        return render(request, 'main/message.html', context={
            'header': Header(
                title='首页_IT小站_专注技术的小博客',
                keywords='it,it小站,通知',
                description='IT小站，专注技术的小博客，这里有你想学的技术，有众多干货分享。'
            ),
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
            'header': Header(
                title='首页_IT小站_专注技术的小博客',
                keywords='it,it小站,通知',
                description='IT小站，专注技术的小博客，这里有你想学的技术，有众多干货分享。'
            ),
            'left_cards': left_cards,
            'right_cards': right_cards
        })


# # github登录回调
# def login_github(request):
#     # 获取 code
#     code = request.GET.get('code')
#     # 准备POST参数用于交换 access_token
#     data = bytes(urllib.parse.urlencode({
#         'client_id': github_client_id,
#         'client_secret': github_client_secret,
#         'code': code
#     }), encoding='utf8')
#     # 发送Http请求用于交换 access_token
#     response = urllib.request.urlopen('https://github.com/login/oauth/access_token', data=data)
#     # 提取 access_token
#     access_token = str(response.read(), encoding='utf-8').split('&')[0].split('=')[1]
#     # 使用 access_token 获取用户信息
#     response = urllib.request.urlopen('https://api.github.com/user?access_token=' + access_token)
#     # 解码成Python对象
#     user_info = json.loads(response.read().decode('utf-8'))
#     user_info['id'] = str(user_info['id'])
#
#     # 查询数据库，看用户是否已经在数据库中
#     # 如果已经有了
#     if KUser.objects.filter(user_type='github', uid=user_info['id']).exists():
#         # 将登陆信息存入 session
#         request.session['login_state'] = True
#         request.session['user_type'] = 'github'
#         request.session['uid'] = user_info['id']
#         request.session['nickname'] = user_info['login']
#         request.session['avatar'] = user_info['avatar_url']
#     # 如果没有
#     else:
#         # 将信息存入 session 和数据库
#         request.session['login_state'] = True
#         request.session['user_type'] = 'github'
#         request.session['uid'] = user_info['id']
#         request.session['nickname'] = user_info['login']
#         request.session['avatar'] = user_info['avatar_url']
#         k_user = KUser(
#             user_type='github',
#             uid=user_info['id'],
#             nickname=user_info['login'],
#             avatar=user_info['avatar_url'])
#         k_user.save()
#
#     # 返回，并且重定向到登录前的网站
#     return HttpResponseRedirect(request.session['login_from'])
#
#
# # qq登录回调
# def login_qq(request):
#     # 获取 code
#     code = request.GET.get('code')
#     # 通过 code 获取Access Token
#     response = urllib.request.urlopen(
#         'https://graph.qq.com/oauth2.0/token?' +
#             'grant_type=authorization_code' +
#             '&client_id=' + qq_client_id +
#             '&client_secret=' + qq_client_secret +
#             '&code=' + code +
#             '&redirect_uri=' + 'http://www.kindemh.cn/login/qq')
#     # 提取 access_token
#     access_token = response.read().decode('utf-8').split('&')[0].split('=')[1]
#     # 使用 access_token 获取用户的 openid
#     response = urllib.request.urlopen(
#         'https://graph.qq.com/oauth2.0/me?' +
#             'access_token=' + access_token
#     )
#
#     # 解码成Python对象
#     json_obj = json.loads(response.read().decode('utf-8').replace('callback( ', '').replace(' );', ''))
#     openid = json_obj['openid']
#
#     # 使用 openid 用户的信息
#     response = urllib.request.urlopen(
#         'https://graph.qq.com/user/get_user_info?' +
#             'access_token=' + access_token +
#             '&oauth_consumer_key=' + qq_client_id +
#             '&openid=' + openid)
#     # 解析成Python对象
#     user_info = json.loads(response.read().decode('utf-8'))
#
#     # 查询数据库，看用户是否已经在数据库之中了
#     # 如果已经有了
#     if KUser.objects.filter(user_type='qq', uid=openid).exists():
#         # 将登录信息存入 session
#         request.session['login_state'] = True
#         request.session['user_type'] = 'qq'
#         request.session['uid'] = openid
#         request.session['nickname'] = user_info['nickname']
#         request.session['avatar'] = user_info['figureurl_qq_1']
#     # 如果有没
#     else:
#         # 将信息存入 session 和数据库
#         request.session['login_state'] = True
#         request.session['user_type'] = 'qq'
#         request.session['uid'] = openid
#         request.session['nickname'] = user_info['nickname']
#         request.session['avatar'] = user_info['figureurl_qq_1']
#         k_user = KUser(
#             user_type='qq',
#             uid=openid,
#             nickname=user_info['nickname'],
#             avatar=user_info['figureurl_qq_1'])
#         k_user.save()
#
#     # 返回，并重定向到登录前的网站
#     return HttpResponseRedirect(request.session['login_from'])


# 注销
# def logout(request):
#     request.session['login_state'] = False
#     request.session['user_type'] = None
#     request.session['uid'] = None
#     request.session['nickname'] = None
#     request.session['avatar'] = None
#     return HttpResponse(json.dumps({
#         'state': True
#     }))



# @csrf_exempt
# # 发表评论
# def publish_comment(request):
#     if request.method == 'POST':
#         obj = json.loads(request.POST['json'])
#         comment = Comment(
#             sender=int(obj['sender']),
#             post=int(obj['post']),
#             level=int(obj['level']),
#             context=str(obj['context'])
#         )
#         # return HttpResponse(str(obj['sender']))
#         comment.save()
#         return HttpResponse(json.dumps({'state': True}))
#     else:
#         return Http404()