class Header:
    """
    页面 header 信息
    """
    def __init__(self, title, keywords, description):
        """
        构造
        :param title: 标题
        :param keywords: 关键词
        :param description: 描述
        """
        self.title = title
        self.keywords = keywords
        self.description = description