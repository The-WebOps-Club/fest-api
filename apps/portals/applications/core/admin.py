#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib import admin
from apps.portals.applications.core.models import *

class SubDeptAdmin(admin.ModelAdmin):
    pass
admin.site.register(SubDept, SubDeptAdmin)

class QuestionAdmin(admin.ModelAdmin):
    pass
admin.site.register(Question, QuestionAdmin)

class CommentsAdmin(admin.ModelAdmin):
    pass
admin.site.register(Comments, CommentsAdmin)

class AppCommentsAdmin(admin.ModelAdmin):
    pass
admin.site.register(AppComments, AppCommentsAdmin)

