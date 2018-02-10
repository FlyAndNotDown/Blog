from main.models import Post
from markdown import markdown
from datetime import datetime
import pytz


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

            # 求时间差
            self.__phase_time = {
                'created': datetime.utcnow().replace(tzinfo=pytz.timezone('UTC')) - post.created_time,
                'modified': datetime.utcnow().replace(tzinfo=pytz.timezone('UTC')) - post.modified_time
            }

            # 封装登录信息
            self.__login_info = LoginInfo(login_state, user_info)


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