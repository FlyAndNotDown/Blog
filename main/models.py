from django.db import models
from django.urls import reverse


# Create your models here.
class Tag(models.Model):
    """
    标签 Model
    # 1. name char(100) 标签名
    """
    # 标签名
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    """
    文章 Model
    # 1. title char(70) 标题
    # 2. body text 正文
    # 3. created_time datetime 创建时间
    # 4. modified_time datetime 最后修改时间
    # 5. tags many2many 标签
    # 6. excerpt 摘要
    """
    # 标题
    title = models.CharField(max_length=70)
    # 正文
    body = models.TextField()
    # 摘要
    excerpt = models.CharField(max_length=200, blank=True)
    # 创建时间
    created_time = models.DateTimeField(auto_now_add=True)
    # 修改时间
    modified_time = models.DateTimeField(auto_now=True)
    # 标签
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('main:post', kwargs={'pk': self.pk})
