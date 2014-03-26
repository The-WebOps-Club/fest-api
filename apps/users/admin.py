from django.contrib import admin

from apps.users.models import Dept, Subdept, UserProfile, ERPProfile

admin.site.register(UserProfile)
admin.site.register(ERPProfile)
admin.site.register(Dept)
admin.site.register(Subdept)
