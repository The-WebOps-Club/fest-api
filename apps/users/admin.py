from django.contrib import admin

from apps.users.models import Dept, Subdept, UserProfile, ERPProfile, Page,Team

def full_name(obj):
    return ("%s %s" % (obj.user.first_name, obj.user.last_name))
full_name.short_description = 'Name'

class UserProfileAdmin(admin.ModelAdmin):
    list_display=('saarang_id',full_name,'user','gender','age','mobile_number','college_text','city')
    search_fields=[full_name,'user','mobile_number']

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(ERPProfile)
admin.site.register(Dept)
admin.site.register(Subdept)
admin.site.register(Page)
admin.site.register(Team)