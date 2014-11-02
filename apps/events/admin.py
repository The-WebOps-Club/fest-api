from django.contrib import admin
from models import EventTab, Event

class EventTabAdmin(admin.ModelAdmin):
    list_display=('pk','event','name' )
admin.site.register(EventTab,EventTabAdmin)

class EventAdmin(admin.ModelAdmin):
    list_display=('pk','name','event_type', "category" )

admin.site.register(Event,EventAdmin)
