from django.contrib import admin

from apps.walls.models import Wall, Post, Comment

admin.site.register(Wall)
admin.site.register(Post)
admin.site.register(Comment)
