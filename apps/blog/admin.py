from django.contrib import admin

from apps.blog.models import Category, Feed

admin.site.register(Category)
admin.site.register(Feed)
