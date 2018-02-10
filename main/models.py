from django.db import models
from django.urls import reverse


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
    # new. keywords char(100) 关键词
    # 3. created_time datetime 创建时间
    # 4. modified_time datetime 最后修改时间
    # 5. tags many2many 标签
    # 6. excerpt 摘要
    """
    # 标题
    title = models.CharField(max_length=70)
    # 关键词
    keywords = models.CharField(max_length=100)
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


class LocalUser(models.Model):
    """
    站点用户 Model
    """
    # 1. username char(20) 用户名(只能为英文和数字)
    # 2. password char(64) 用户密码的 SHA256+salt Hash值
    # 3. salt char(16) 盐
    # 4. avatar char(100) 用户头像
    # 5. is_admin bool 是否为管理员
    # 用户名
    username = models.CharField(max_length=20)
    # 用户密码的 SHA256+salt Hash值
    password = models.CharField(max_length=64)
    # 盐
    salt = models.CharField(max_length=16)
    # 头像
    avatar = models.CharField(max_length=100, blank=True)
    # 是否为管理员
    is_admin = models.BooleanField()


class KUser(models.Model):
    """
    用户 Model
    """
    # 1. user_type char(10) 用户类型(取值可能为 local、qq、github、wechat、weibo等)
    # 2. nickname char(20) 昵称
    # 3. uid char(50) 用户唯一ID
    # 4. avatar char(100) 用户头像
    # 5. is_admin bool 是否为管理员
    # 用户类型
    user_type = models.CharField(max_length=10)
    # 昵称
    nickname = models.CharField(max_length=20)
    # 用户唯一 id
    uid = models.CharField(max_length=50)
    # 用户头像
    avatar = models.CharField(max_length=100, blank=True)
    # 是否为管理员
    is_admin = models.BooleanField()



class Comment(models.Model):
    """
    评论 Model
    """
    # 1. sender integer 发送者 KUser pk
    # 2. receiver integer 接受者 KUser pk
    # 3. post integer 所在文章 pk
    # 4. is_child bool 是否为二级评论
    # 5. parent integer 父级评论 pk
    # 6. context text 评论内容
    # 7. have_been_read bool 是否已经被接受者阅读
    # 发送者 pk
    sender = models.IntegerField()
    # 接受者 pk
    receiver = models.IntegerField(blank=True, null=True)
    # 所在文章 pk
    post = models.IntegerField()
    # 是否为二级评论
    is_child = models.BooleanField()
    # 父级评论 pk
    parent = models.IntegerField(blank=True, null=True)
    # 评论内容
    context = models.TextField()
    # 是否已经被接受者阅读
    have_been_read = models.BooleanField(default=False)


# class KUser(models.Model):
#     """
#     用户 Model
#     # 1. user_type char(10) 用户类型
#     # 2. nickname char(20) 昵称
#     # 3. uid char(50) 用户唯一ID
#     # 4. avatar char(100) 用户头像
#     # 5. is_admin bool 是否为管理员
#     """
#     # 用户类型
#     user_type = models.CharField(max_length=10)
#     # 昵称
#     nickname = models.CharField(max_length=20)
#     # 用户唯一ID
#     uid = models.integer = models.CharField(max_length=50)
#     # 用户头像
#     avatar = models.CharField(max_length=100)
#     # 是否为管理员
#     is_admin = models.BooleanField()
#
#
# class Comment(models.Model):
#     """
#     评论 Model
#     # 1. sender Integer发送者PK
#     # 2. receiver Integer 接受者PK
#     # 3. post integer 所在文章PK
#     # 4. level integer 评论继承等级(1为父级，2位子级)
#     # 5. parent integer 父级评论PK
#     # 5. time datetime 评论发表时间
#     # 6. context text 评论内容
#     """
#     # 发送者PK
#     sender = models.IntegerField()
#     # 接受者PK
#     receiver = models.IntegerField(blank=True, null=True)
#     # 所在文章PK
#     post = models.IntegerField()
#     # 评论继承等级
#     level = models.IntegerField()
#     # 父级评论PK
#     parent = models.IntegerField(blank=True, null=True)
#     # 评论发表时间
#     time = models.DateTimeField(auto_now_add=True)
#     # 评论内容
#     context = models.CharField(max_length=500)
#     # 是否已经阅读
#     have_read = models.BooleanField()