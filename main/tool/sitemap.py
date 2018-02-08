from main.models import Post
from django.contrib.sitemaps import Sitemap
from datetime import datetime


# 定制的 Sitemap
class PostSitemap(Sitemap):
    changeFreq = 'daily'
    priority = 0.5

    def items(self):
        return Post.objects.all()

    def lastmod(self, obj):
        return obj.modified_time

    def location(self, obj):
        return "/post/" + str(obj.pk)


class MainSitemap(Sitemap):
    changeFreq = 'daily'
    priority = 0.5

    def items(self):
        return ['/', '/archive', '/about']

    def lastmod(self, obj):
        return datetime.now()

    def location(self, obj):
        return obj