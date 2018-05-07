from main.models import Post
from django.core.paginator import Paginator


# 首页每一页的文章数量
INDEX_POST_PER_PAGE = 8
# 博客诞生年份
BLOG_START_YEAR = 2018

# 主页标语
SLOGAN = 'A geek who wanna to be a geek!'

class IndexSloganBox:
    """
    主页标语
    """
    def __init__(self):
        self.slogan = SLOGAN


class IndexPageInfo:
    """
    分页信息
    """
    def __init__(self, current, is_first, is_last):
        """
        构造
        :param current: 当前页数
        :param is_first: 是否为第一页
        :param is_last: 是否为最后一页
        """
        self.current = current
        self.is_first = is_first
        self.is_last = is_last
        self.pre = current - 1
        self.next = current + 1


class IndexPostList:
    """
    文章列表
    """
    def __init__(self, all, left, right):
        """
        构造
        :param all: 所有文章
        :param left: 左边的文章
        :param right: 右边的文章
        """
        self.all = list()
        self.all.extend(all)
        self.left = list()
        self.left.extend(left)
        self.right = list()
        self.right.extend(right)


class IndexRender:
    """
    主页渲染器
    """
    def __init__(self, request_page):
        """
        构造
        :param request_page: 请求的页数
        """
        self.__request_page = request_page
        self.__error = False

        request_page = int(request_page)

        # 获取所有文章
        posts = Post.objects.all().order_by('-created_time')
        # 获取总页数
        page_total = (len(posts) - 1)// INDEX_POST_PER_PAGE + 1
        # 错误检测
        if not (0 < request_page <= page_total):
            self.__error = True
        else:
            # 用分页器取得请求页的文章
            paginator = Paginator(posts, INDEX_POST_PER_PAGE)
            posts_this_page = paginator.page(request_page)

            # 判断是否为第一页或者最后一页
            is_first_page = request_page == 1
            is_last_page = request_page == page_total
            # 存储页信息
            self.__page_info = IndexPageInfo(request_page, is_first_page, is_last_page)

            # 文章排序
            posts_left = list()
            posts_right = list()
            for i in range(0, len(posts_this_page)):
                if i % 2 == 0:
                    posts_left.append(posts_this_page[i])
                else:
                    posts_right.append(posts_this_page[i])
            # 存储文章信息
            self.__post_list = IndexPostList(posts_this_page, posts_left, posts_right)

    def error_happen(self):
        """
        是否有错误发生
        :return: True/False
        """
        return self.__error

    def get_page_info(self):
        """
        获取分页信息
        :return: IndexPageInfo
        """
        return self.__page_info

    def get_post_list(self):
        """
        获取文章列表
        :return: IndexPostList
        """
        return self.__post_list
