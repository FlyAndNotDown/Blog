from main.models import LocalUser, KUser


# 登录参数
# github
github_param = {
    'client_id': '2b18fc8f7305f2e73416',
    'client_secret': 'eee6029f6f6f5873cc3fc8fcf9ebdb86ef375349'
}
# qq
qq_param = {
    'client_id': '101456289',
    'client_secret': 'b26af05256f42dce9c81e5fcc4db0195'
}


class LoginLocalRegisterRequest:
    """
    登录系统-本站用户注册请求
    """
    def __init__(self, username, password, salt):
        # 检验数据库中是否已经存在该用户
        if LocalUser.objects.filter(username=username):
            self.__response = {
                'state': False,
                'reason': '该用户名已经被注册过了，换一个吧!'
            }
        else:
            # 将用户信息存入数据库
            local_user = LocalUser(
                username=username,
                password=password,
                salt=salt,
                is_admin=False
            )
            local_user.save()
            k_user = KUser(
                user_type='local',
                nickname=local_user.username,
                uid=local_user.pk,
                is_admin=local_user.is_admin
            )
            k_user.save()
            self.__user_info = {
                'user_type': k_user.user_type,
                'nickname': k_user.nickname,
                'uid': k_user.uid,
                'avatar': k_user.avatar,
                'is_admin': k_user.is_admin
            }
            # 返回注册成功信息
            self.__response = {
                'state': True
            }

    def get_response(self):
        return self.__response

    def get_user_info(self):
        return self.__user_info


class LoginLocalGetSaltRequest:
    """
    本站登录-获取 salt 请求
    """
    def __init__(self, username):
        """
        构造
        :param username: 用户名
        """
        # 如果用户存在
        if LocalUser.objects.filter(username=username).exists():
            # 查询用户对应的 salt
            local_user = LocalUser.objects.get(username=username)
            salt = local_user.salt
            # 返回数据
            self.__response = {
                'state': True,
                'salt': salt
            }

        # 如果用户不存在
        else:
            self.__response = {
                'state': False,
                'reason': '用户不存在!'
            }

    def get_response(self):
        return self.__response


class LoginLocalLoginRequest:
    """
    本站登录验证请求
    """
    def __init__(self, username, password):
        """
        构造
        :param username: 用户名
        :param password: 密码(的SHA256 Hash值)
        """
        # 查询数据库，看用户名和密码是否匹配
        if LocalUser.objects.filter(username=username, password=password).exists():
            local_user = LocalUser.objects.get(username=username, password=password)
            # 返回数据
            self.__response = {
                'state': True
            }
            self.__user_info = {
                'user_type': 'local',
                'nickname': local_user.username,
                'uid': local_user.pk,
                'avatar': local_user.avatar,
                'is_admin': local_user.is_admin
            }
        else:
            self.__response = {
                'state': False,
                'reason': '用户名或密码错误!'
            }

    def get_response(self):
        return self.__response

    def get_user_info(self):
        return self.__user_info
