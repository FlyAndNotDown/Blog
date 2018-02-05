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


class KUser(models.Model):
    """
    用户 Model
    # 1. user_type char(10) 用户类型
    # 2. nickname char(20) 昵称
    # 3. uid integer 用户唯一ID
    # 4. avatar char(100) 用户头像
    """
    # 用户类型
    user_type = models.CharField(max_length=10)
    # 昵称
    nickname = models.CharField(max_length=20)
    # 用户唯一ID
    uid = models.integer = models.CharField(max_length=20)
    # 用户头像
    avatar = models.CharField(max_length=100)


class Comment(models.Model):
    """
    评论 Model
    # 1. sender Integer发送者PK
    # 2. receiver Integer 接受者PK
    # 3. post integer 所在文章PK
    # 4. level integer 评论继承等级(1为父级，2位子级)
    # 5. parent integer 父级评论PK
    # 5. time datetime 评论发表时间
    # 6. context text 评论内容
    """
    # 发送者PK
    sender = models.IntegerField()
    # 接受者PK
    receiver = models.IntegerField()
    # 所在文章PK
    post = models.IntegerField()
    # 评论继承等级
    level = models.IntegerField()
    # 父级评论PK
    parent = models.IntegerField()
    # 评论发表时间
    time = models.DateTimeField()
    # 评论内容
    context = models.CharField(max_length=500)
