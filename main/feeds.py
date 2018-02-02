from django.contrib.syndication.views import Feed
from .models import Post
import markdown


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
        item.body = markdown.markdown(
            item.body,
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
        return item.body
