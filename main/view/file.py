from datetime import datetime
import os


site_url = 'http://www.kindemh.cn'
picture_path = '/static/main/img/'



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
            return True
    return False


def get_file_name_by_time():
    """
    根据当前时间获取一个文件名
    :return: 文件名
    """
    time_now = datetime.now()
    return str(time_now.year) + '-' + str(time_now.month) + '-' + str(time_now.day) + '_' +\
        str(time_now.hour) + '-' + str(time_now.minute) + '-' + str(time_now.second)


class PictureUploadRequest:
    """
    图片上传请求
    """
    def __init__(self, picture):
        """
        文件
        :param picture: 图片
        """
        # 先检查文件是否有危害
        if check_if_file_dangerous(picture.name):
            self.__response = {
                'state': False,
                'reason': '图片类型对服务器有危害，禁止上传!'
            }
        else:
            try:
                file_name = str(get_file_name_by_time()) + str(get_file_postfix(picture.name))
                f = open(os.path.join('main', 'static', 'main', 'img', file_name), 'wb')
                for chunk in picture.chunks(chunk_size=1024):
                    f.write(chunk)
                f.close()
                self.__response = {
                    'state': True,
                    'url': site_url + picture_path + file_name
                }
            except Exception:
                self.__response = {
                    'state': False,
                    'reason': '服务器保存图片时出现异常!'
                }
                return

    def get_response(self):
        return self.__response
