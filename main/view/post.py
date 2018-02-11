from main.models import Post, Comment, KUser
from markdown import markdown
from datetime import datetime, timezone, timedelta
import pytz


# 中国时区信息
timezone_delta_hour = 8


class LoginInfo:
    """
    登录信息
    """
    def __init__(self, login_state, user_info):
        """
        构造
        :param login_state: 用户是否登录
        :param user_info: 登录用户的信息
        """
        self.login_state = login_state
        self.user_info = user_info


class PostRender:
    """
    文章页面渲染器
    """
    def __init__(self, pk, login_state, user_info):
        """
        构造
        :param pk: 文章主键
        :param login_state: 用户是否登录
        :param user_info: 登录用户的信息
        """
        self.__error = False
        # 错误判断
        if not Post.objects.filter(pk=pk).exists():
            self.__error = True
        else:
            # 获取文章 Model 对象
            post = Post.objects.get(pk=pk)
            # Markdown 渲染
            post.body = markdown(
                post.body,
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
            self.__post = post

            phase_created = datetime.utcnow().replace(tzinfo=pytz.timezone('UTC')) - post.created_time
            phase_modified = datetime.utcnow().replace(tzinfo=pytz.timezone('UTC')) - post.modified_time
            # 求时间差
            self.__phase_time = {
                'created': {
                    'days': phase_created.days,
                    'hours': phase_created.seconds // 3600
                },
                'modified': {
                    'days': phase_modified.days,
                    'hours': phase_modified.seconds // 3600
                }
            }

            # 封装登录信息
            self.__login_info = LoginInfo(login_state, user_info)

            # 获取评论信息
            # 先获取所有该文章下的评论
            comments = Comment.objects.filter(post=pk)
            # 筛选出所有的一级评论
            comments_level_1 = comments.filter(is_child=False).order_by('-time')
            # 建立评论表数据结构
            self.__comments = []
            # 遍历所有一级评论，找到他们下的二级评论，并且按照数据结构存入
            for comment in comments_level_1:
                self.__comments.append({})
                self.__comments[-1]['parent'] = comment
                self.__comments[-1]['children'] = []
                # 寻找他们下面的二级评论
                children = Comment.objects.filter(is_child=True, parent=comment.pk)
                # 将二级评论全部存入数据结构中
                for child in children:
                    self.__comments[-1]['children'].append(child)

            # 获取中国时区信息
            timezone_china = timezone(timedelta(hours=timezone_delta_hour))
            # 处理数据，过滤掉不需要的数据
            for comment_dict in self.__comments:
                # 先处理一级评论
                obj1 = KUser.objects.get(pk=comment_dict['parent'].sender)
                new_parent = {
                    'sender': {
                        'user_type': obj1.user_type,
                        'nickname': obj1.nickname,
                        'uid': obj1.uid,
                        'avatar': obj1.avatar,
                        'is_admin': obj1.is_admin
                    },
                    'is_child': False,
                    'context': comment_dict['parent'].context,
                    'time': comment_dict['parent'].time.astimezone(timezone_china)
                }
                comment_dict['parent'] = new_parent
                # 再处理二级评论
                for child in comment_dict['children']:
                    obj1 = KUser.objects.get(pk=child.sender)
                    obj2 = KUser.objects.get(pk=child.receiver)
                    new_child = {
                        'sender': {
                            'user_type': obj1.user_type,
                            'nickname': obj1.nickname,
                            'uid': obj1.uid,
                            'avatar': obj1.avatar,
                            'is_admin': obj1.is_admin
                        },
                        'receiver': {
                            'user_type': obj2.user_type,
                            'nickname': obj2.nickname,
                            'uid': obj2.uid,
                            'avatar': obj2.avatar,
                            'is_admin': obj2.is_admin
                        },
                        'is_child': True,
                        'context': child.context,
                        'time': child.time.astimezone(timezone_china)
                    }
                    child = new_child

    def error_happen(self):
        """
        是否发生错误
        :return: True/False
        """
        return self.__error

    def get_post(self):
        """
        获取文章内容
        :return: Post
        """
        return self.__post

    def get_phase_time(self):
        """
        获取时间差
        :return: phase_time
        """
        return self.__phase_time

    def get_login_info(self):
        """
        获取登录信息
        :return: 登录信息
        """
        return self.__login_info

    def get_comments(self):
        """
        获取评论信息
        :return: 评论信息
        """
        return self.__comments
