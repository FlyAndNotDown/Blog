from main.models import LocalUser, KUser
import urllib.request
import urllib.response
import urllib.parse
import json


# 登录参数
# github
github_param = {
    'client_id': '2b18fc8f7305f2e73416',
    'client_secret': 'eee6029f6f6f5873cc3fc8fcf9ebdb86ef375349'
}
# qq
qq_param = {
    'client_id': '101456289',
    'client_secret': 'b26af05256f42dce9c81e5fcc4db0195',
    'callback': 'http://www.kindemh.cn/login/qq/callback'
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
                'is_admin': k_user.is_admin,
                'pk': k_user.pk
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
                'is_admin': local_user.is_admin,
                'pk': local_user.pk
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


class LoginGitHubCallbackRequest:
    """
    GitHub 登录回调
    """
    def __init__(self, code):
        """
        构造
        :param code: code
        """
        self.__response = {}
        # 准备 POST 参数用于交换 access_token
        data = bytes(urllib.parse.urlencode({
            'client_id': github_param['client_id'],
            'client_secret': github_param['client_secret'],
            'code': code
        }), encoding='utf8')
        try:
            # 发送 http 请求用于交换 access_token
            response = urllib.request.urlopen('https://github.com/login/oauth/access_token', data=data)
            # 提取 access_token
            access_token = str(response.read(), encoding='utf-8').split('&')[0].split('=')[1]
            # 使用 access_token 获取用户信息
            response = urllib.request.urlopen('https://api.github.com/user?access_token=' + access_token)
            # 解码成 Python 对象
            user_info = json.loads(response.read().decode('utf-8'))

            # 用 id 来校验是否登录成功
            if user_info.get('id'):
                user_info['id'] = str(user_info['id'])
                self.__response['success'] = True

                # 查询数据库，看用户是否已经在数据库中
                if not KUser.objects.filter(user_type='github', uid=user_info['id']).exists():
                    # 将用户信息存入数据库
                    k_user = KUser(
                        user_type='github',
                        uid=user_info['id'],
                        nickname=user_info['login'],
                        avatar=user_info['avatar_url'],
                        is_admin=False
                    )
                    k_user.save()
                else:
                    k_user = KUser.objects.get(user_type='github', uid=user_info['id'])
                self.__response['user_info'] = {
                    'user_type': k_user.user_type,
                    'uid': k_user.uid,
                    'nickname': k_user.nickname,
                    'avatar': k_user.avatar,
                    'is_admin': k_user.is_admin,
                    'pk': k_user.pk
                }
            else:
                self.__response['success'] = False
        except Exception:
            self.__response['success'] = False
            return

    def get_response(self):
        """
        获取 response
        :return: response
        """
        return self.__response


class LoginQQCallbackRequest:
    """
    QQ 登录回调
    """
    def __init__(self, code):
        """
        构造
        :param code: code
        """
        self.__response = {}
        try:
            # 通过 code 获取 access_token
            response = urllib.request.urlopen(
                'https://graph.qq.com/oauth2.0/token?' +
                    'grant_type=authorization_code' +
                    '&client_id=' + qq_param['client_id'] +
                    '&client_secret=' + qq_param['client_secret'] +
                    '&code=' + code +
                    '&redirect_uri=' + qq_param['callback']
            )
            # 提取 access_token
            access_token = response.read().decode('utf-8').split('&')[0].split('=')[1]
            # 使用 access_token 获取用户的 openid
            response = urllib.request.urlopen(
                'https://graph.qq.com/oauth2.0/me?' +
                    'access_token=' + access_token
            )

            # 解码成 Python 对象
            json_obj = json.loads(response.read().decode('utf-8').replace('callback( ', '').replace(' );', ''))
            open_id = json_obj['openid']

            # 使用 openid 获取用户的信息
            response = urllib.request.urlopen(
                'https://graph.qq.com/user/get_user_info?' +
                    'access_token=' + access_token +
                    '&oauth_consumer_key=' + qq_param['client_id'] +
                    '&openid=' + open_id
            )
            # 解码成 Python 对象
            user_info = json.loads(response.read().decode('utf-8'))

            # 使用 user_info 中的 nickname 来校验是否登录成功
            if user_info['nickname']:
                self.__response['success'] = True
                # 查询数据库，看数据库中是否已经有用户数据了
                if KUser.objects.filter(user_type='qq', uid=open_id).exists():
                    # 如果已经有了，就直接取用户出来
                    k_user = KUser.objects.get(user_type='qq', uid=open_id)
                else:
                    # 如果没有，那么就将用户存入数据库
                    k_user = KUser(
                        user_type='qq',
                        uid=open_id,
                        nickname=user_info['nickname'],
                        avatar=user_info['figureurl_qq_1'],
                        is_admin=False
                    )
                    k_user.save()
                self.__response['user_info'] = {
                    'user_type': k_user.user_type,
                    'uid': k_user.uid,
                    'nickname': k_user.nickname,
                    'avatar': k_user.avatar,
                    'is_admin': k_user.is_admin,
                    'pk': k_user.pk
                }
            else:
                self.__response['success'] = False
        except Exception:
            self.__response['success'] = False
            return

    def get_response(self):
        return self.__response
