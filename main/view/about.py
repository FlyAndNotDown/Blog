admin_info = {
    'name': '站主:Kindem',
    'slogan': '一只想做全栈开发者的野生程序猿',
    'introduction': '男，20岁，南京航空航天大学计算机学院在校本科生，目前大三，热爱生活，热爱编程，热爱ACG。喜欢学习新技术，'
                    '自己捣鼓项目，学习过很多门编程语言，接触过很多技术。最喜欢的技术是Web开发和游戏开发。最大的梦想是能够成为'
                    '一名全栈开发或是一名游戏开发者。审美上对Material Design没有抵抗力。',
    'experiences': [{
        'start_year': 2018,
        'long': 4,
        'location': '南京航空航天大学',
        'do': '大学本科'
    }],
    'skills': {
        'languages': [
            'C', 'C++', 'C#', 'Java', 'Kotlin', 'Python', 'HTML', 'CSS',
            'JavaScript', 'Markdown', 'SQL', 'Arduino', 'Assembly', 'JSX'
        ],
        'libs': [
            'jQuery', 'Bootstrap', 'Materialize', 'Django', 'OpenCV', 'React', 'Webpack'
        ],
        'tools': [
            'IDEA', 'WebStorm', 'PyCharm', 'Android Studio', 'Visual Studio',
            'Visual Studio Code', 'Unity3D', 'Vim'
        ]
    }
}


class AboutSloganBox:
    """
    关于页面标语
    """
    def __init__(self):
        """
        构造
        """
        self.name = admin_info['name']
        self.slogan = admin_info['slogan']


class AboutIntroductionBox:
    """
    关于页面介绍
    """
    def __init__(self):
        """
        构造
        """
        self.introduction = admin_info['introduction']


class AboutExperienceBox:
    """
    关于页面履历
    """
    def __init__(self):
        """
        构造
        """
        self.experiences = list()
        for experience in admin_info['experiences']:
            self.experiences.append({
                'start_year': experience['start_year'],
                'long': experience['long'],
                'location': experience['location'],
                'do': experience['do']
            })


class AboutSkillBox:
    """
    关于页面技能点
    """
    def __init__(self):
        """
        构造
        """
        self.languages = list()
        self.libs = list()
        self.tools = list()
        for l in admin_info['skills']['languages']:
            self.languages.append(l)
        for l in admin_info['skills']['libs']:
            self.libs.append(l)
        for t in admin_info['skills']['tools']:
            self.tools.append(t)
