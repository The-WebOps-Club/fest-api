from django.contrib import admin

from apps.users.models import Dept, Subdept, UserProfile, ERPProfile, Page

admin.site.register(UserProfile)
admin.site.register(ERPProfile)
admin.site.register(Dept)
admin.site.register(Subdept)
admin.site.register(Page)