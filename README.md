# 说明
这是一个基于Python+Django实现的Web个人博客，我的博客就是使用这个项目部署的，网站地址在[Kindem的个人博客](http://www.kindemh.cn/)，欢迎大家访问、提出意见

# 运行
确保你安装了python3，接下来使用pip安装一些依赖:
```
// windows
pip install django
pip install markdown

// linux
pip3 install django
pip3 install markdown
```

接下来，进入项目根目录，运行迁移数据库指令:
```
// 生成数据库迁移描述文件
python manage.py makemigrations
// 进行数据库迁移
python manage.py migrate
```

接着进入settings.py打开调试模式:
```
// /Blog/settings/py
DEBUG = True
```

创建django admin账户:
```
python manage.py createsuperuser
// ...按照提示输入信息
```

收集静态文件
```
python manage.py collectstatic
```

开启调试服务器
```
python manage.py runserver 8000
```

使用admin账户登录[http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)，在里面新建一篇文章(貌似我写的时候有bug，没有文章会自动跳404)

可以看到文章就说明运行成功了。

# 部署
如果你要拿我的项目搭建自己博客的话，还需要改很多东西：
* 链接：我的链接为了SEO优化全部写的自己的域名加上path，你自己运行的时候动不动就会跳到我的博客去，所以你需要改成你自己的链接
* 静态内容：有一些相对稳定的内容我直接写入了静态html中，比如个人联系方式、友链等，你需要自己改成自己的
* 第三方登录：第三方登录需要验证域，所以必须嵌入代码中，你需要自己申请第三方登录api权限并且把第三方登录的登录凭据也改成自己的

完成这些之后，你还需要购买域名、建立服务器并且使用nginx和gunicorn做端口代理和并发处理等，具体的你可以参照这位大大的文章：[使用 Nginx 和 Gunicorn 部署 Django 博客 - 追梦人物的博客](https://www.zmrenwu.com/post/20/)，

毕竟我的博客就是参照这篇文章为框架做的。

另外，enjoy项目，觉得不错别忘了给个star哦!