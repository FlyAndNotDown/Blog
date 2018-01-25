from django.contrib import admin
from .models import Post, Tag


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_time', 'modified_time']


class TagAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
