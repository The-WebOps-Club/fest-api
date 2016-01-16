from django.contrib import admin
from models import EventTab, Event, EventRegistration, EventSchedule, EventWinner, WebsiteUpdate,EventParticipation, EventFeedback

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

class EventWinnerAdmin(admin.ModelAdmin):
    list_display=('pk','event', 'position', 'added_by', 'comment', 'user')
admin.site.register(EventWinner, EventWinnerAdmin)
class WebsiteUpdateAdmin(admin.ModelAdmin):
    list_display=('pk','type','title','text')
admin.site.register(WebsiteUpdate, WebsiteUpdateAdmin)

admin.site.register(EventParticipation)

class EventFeedbackAdmin(admin.ModelAdmin):
    list_display=('pk','event','q1','q2','q3','q4','q5')
admin.site.register(EventFeedback, EventFeedbackAdmin)
