def get_file_postfix(file_name):
    """
    获取后缀名
    :param file_name: 文件名
    :return: 后缀名
    """
    return '.' + file_name.split('.')[-1]


# 危险的文件后缀名
dangerous_file_postfix = [
    '.sh'
]


def check_if_file_dangerous(file_name):
    """
    检验文件是否危险
    :param file_name: 文件名
    :return: 是否危险
    """
    postfix = get_file_postfix(file_name)
    for p in dangerous_file_postfix:
        if postfix == p:
            return False
    return True


# TODO 获取随机名字


class FileUploadRequest:
    """
    文件上传请求
    """
    def __init__(self, file, file_type):
        """
        文件
        :param file: 文件
        :param file_type: 文件类型
        """
        # 先检查文件是否有危害
        if check_if_file_dangerous(file.name):
            self.__response = {
                'state': False,
                'reason': '文件类型对服务器有危害，禁止上传'
            }
        else:
            # TODO
            pass
