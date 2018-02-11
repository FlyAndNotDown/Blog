from main.models import Comment


class CommentPublishRequest:
    """
    发表评论请求
    """
    def __init__(self, sender, post, context):
        """
        构造
        :param sender: 发送者 pk
        :param post: 文章 pk
        :param context: 评论内容
        """
        # 将数据存入数据库
        comment = Comment(
            sender = sender,
            post=post,
            is_child=False,
            context=context,
        )
        comment.save()
