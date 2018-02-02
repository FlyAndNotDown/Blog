from django.contrib.syndication.views import Feed
from .models import Post


# RSS 订阅
class AllPostRssFeed(Feed):
    """
    所有文章的RSS Feed
    """
    # 显示在RSS阅读器上的标题
    title = 'Kindem的博客'
    # 通过RSS阅读器跳转到的网址
    link = '/'
    # 显示在RSS阅读器上的描述信息
    description = '一个认真的技术博客'

    # 需要显示的内容条目
    def items(self):
        return Post.objects.all()

    # RSS阅读器中显示的内容的标题
    def item_title(self, item):
        return '[%s.%s] %s' % (item.created_time.month, item.created_time.day, item.title)

    # RSS阅读器中内容条目的描述
    def item_description(self, item):
        return item.body
