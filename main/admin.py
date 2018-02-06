from django.contrib import admin
from .models import Post, Tag, KUser, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_time', 'modified_time']


class TagAdmin(admin.ModelAdmin):
    list_display = ['name']

class KUserAdmin(admin.ModelAdmin):
    list_display = ['user_type', 'nickname', 'uid', 'avatar']

class CommentAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'post', 'level', 'parent', 'time', 'context']


admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(KUser, KUserAdmin)
admin.site.register(Comment, CommentAdmin)
