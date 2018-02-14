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


class CommentReplyRequest:
    """
    回复评论请求
    """
    def __init__(self, sender, receiver, post, parent, context):
        """
        构造
        :param sender: 发送者 pk
        :param receiver: 接收者 pk
        :param post: 文章 pk
        :param parent: 父级评论 pk
        :param context: 评论
        """
        # 将数据存入数据库
        comment = Comment(
            sender=sender,
            receiver=receiver,
            post=post,
            is_child=True,
            parent=parent,
            context=context
        )
        comment.save()
