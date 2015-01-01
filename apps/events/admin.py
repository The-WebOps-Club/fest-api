from django.contrib import admin
from models import EventTab, Event, EventRegistration, EventSchedule, WebsiteUpdate

class EventTabAdmin(admin.ModelAdmin):
    list_display=('pk','event','name' )
admin.site.register(EventTab,EventTabAdmin)

class EventAdmin(admin.ModelAdmin):
    list_display=('pk','name','event_type', "category" )
admin.site.register(Event,EventAdmin)

class EventRegistrationAdmin(admin.ModelAdmin):
    list_display=('pk','event', 'users_registered', 'info', 'teams_registered')
    search_fields=['users_registered']
admin.site.register(EventRegistration, EventRegistrationAdmin)

class EventScheduleAdmin(admin.ModelAdmin):
    list_display=('pk','event', 'slot_start', 'slot_end', 'comment')
admin.site.register(EventSchedule, EventScheduleAdmin)

class WebsiteUpdateAdmin(admin.ModelAdmin):
    list_display=('pk','type','title','text')
admin.site.register(WebsiteUpdate, WebsiteUpdateAdmin)
