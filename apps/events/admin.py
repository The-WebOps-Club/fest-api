from django.contrib import admin
from models import EventTab

class EventTabAdmin(admin.ModelAdmin):
    list_display=('pk','event','name' )
admin.site.register(EventTab,EventTabAdmin)
