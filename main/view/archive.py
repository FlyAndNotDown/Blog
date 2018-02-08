from main.models import Post
from datetime import datetime


# 博客开始工作的年份
BLOG_START_YEAR = 2018
# 标语
SLOGAN = '历史总是有趣的'


class ArchiveSloganBox:
    """
    归档标语
    """
    def __init__(self):
        self.slogan = SLOGAN


class ArchivePostsInYear:
    """
    一年中的所有文章
    """
    def __init__(self, year, posts=()):
        """
        构造
        :param posts: 这一年发布的所有文章
        :param year: 年份
        """
        self.posts = list()
        self.posts.extend(posts)
        self.year = year

    def append(self, post):
        """
        添加一片文章到该集合
        :param post: 文章
        """
        self.posts.append(post)


class ArchiveRender:
    """
    归档页面渲染器
    """
    def __init__(self):
        # 获取所有文章
        posts = Post.objects.all().order_by('-created_time')

        # 获取当前年份
        year_now = datetime.now().year

        # 按照年份分类文章
        self.__posts_every_year = list()
        for i in range(0, year_now + 1 - BLOG_START_YEAR):
            self.__posts_every_year.append(ArchivePostsInYear(BLOG_START_YEAR + i))
            for p in posts.filter(created_time__year=BLOG_START_YEAR + i):
                self.__posts_every_year[i].append(p)

    def get_posts_every_year(self):
        """
        获取每一年的文章
        :return: list of ArchivePostInYear
        """
        return self.__posts_every_year
