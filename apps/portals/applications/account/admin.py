#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib import admin
from apps.portals.applications.account.models import *

class AnnouncementAdmin(admin.ModelAdmin):
    pass
admin.site.register(Announcement, AnnouncementAdmin)

class UserProfileAdmin(admin.ModelAdmin):
    pass
admin.site.register(UserProfile, UserProfileAdmin)
