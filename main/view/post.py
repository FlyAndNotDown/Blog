from main.models import Post
from markdown import markdown
from datetime import datetime
import pytz


class PostRender:
    """
    文章页面渲染器
    """
    def __init__(self, pk):
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