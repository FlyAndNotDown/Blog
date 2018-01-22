from django.db import models


# Create your models here.
class Tag(models.Model):
    """
    标签 Model
    # 1. name char(100) 标签名
    """
    # 标签名
    name = models.CharField(max_length=100)


class Image(models.Model):
    """
    图片 Model
    1. location char(200) 图片位置
    """
    # 图片位置
    location = models.CharField(max_length=200)


class Post(models.Model):
    """
    文章 Model
    # 1. title char(70) 标题
    # 2. body text 正文
    # 3. created_time datetime 创建时间
    # 4. modified_time datetime 最后修改时间
    # 5. tags many2many 标签
    # 6. images many2many 图片
    """
    # 标题
    title = models.CharField(max_length=70)
    # 正文
    body = models.TextField()
    # 创建时间
    created_time = models.DateTimeField()
    # 修改时间
    modified_time = models.DateTimeField()
    # 标签
    tags = models.ManyToManyField(Tag, blank=True)
    # 图片
    images = models.ManyToManyField(Image, blank=True)