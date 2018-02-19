from main.models import Comment, KUser, Post
from .login import qq_param, github_param


class MessageRender:
    """
    通知页面请求
    """
    def __init__(self, login_state, user_info):
        """
        构造
        :param login_state: 登录状态
        :param user_info: 登录用户信息
        """
        self.__card_info = {
            'left': [],
            'right': [],
            'all': []
        }
        # 根据是否登录来做出不同的渲染响应
        # 如果已经登录了
        if login_state:
            # 获取有关用户的通知
            messages = Comment.objects.all().filter(receiver=user_info['pk'], is_child=True)
            # 添加卡片
            for message in messages:
                self.__card_info['all'].append({
                    'body': {
                        'title': 'From ' + KUser.objects.get(pk=message.sender).nickname,
                        'content': '(Ta在文章《' + Post.objects.get(pk=message.post).title + '》中回复你): ' + message.context,
                        'is_login': False
                    },
                    'links': [{
                        'name': '查看',
                        'href': '/post/' + str(message.post)
                    }]
                })

        # 将弄好的 all 分配到左右两边的卡片槽去
        for i in range(0, len(self.__card_info['all'])):
            if i % 2 == 0:
                self.__card_info['right'].append(self.__card_info['all'][i])
            else:
                self.__card_info['left'].append(self.__card_info['all'][i])

    def get_card_info(self):
        return self.__card_info
