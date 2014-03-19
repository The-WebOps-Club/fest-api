from django.contrib import admin

from apps.users.models import Dept, Subdept, UserProfile, ERPUser

admin.site.register(UserProfile)
admin.site.register(ERPUser)
admin.site.register(Dept)
admin.site.register(Subdept)
