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

class LoginRegisterLocalRequest:
    """
    登录系统-本站用户注册请求
    """
    def __init__(self, username, password, salt):
        # 错误检测
        if username is None or password is None or salt is None:
            self.__response = {
                'state': False,
                'reason': '注册时客户端出错!'
            }
        else:
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
                    nickname=username,
                    uid=local_user.pk,
                    is_admin=False
                )
                k_user.save()
                self.__save_obj = k_user
                # 返回注册成功信息
                self.__response = {
                    'state': True
                }

    def get_response(self):
        return self.__response

    def get_save_obj(self):
        return self.__save_obj
