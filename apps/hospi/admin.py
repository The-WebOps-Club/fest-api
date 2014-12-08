from django.contrib import admin

from apps.hospi.models import Hostel, Room, HospiTeam, Allotment, HospiLog

class HospiTeamAdmin(admin.ModelAdmin):
    list_display=('team_sid', 'name', 'leader', 'accomodation_status')
    search_fields = ['team_sid', 'name', 'leader']

class AllotmentAdmin(admin.ModelAdmin):
    list_display = ('team', 'alloted_by', 'timestamp')
    search_fields = ['team', 'alloted_by']

class HospiLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'created_by', 'user', 'room', 'checked_out', 'checkout_time', 'checked_out_by')
    search_fields = ['created_by', 'user', 'room', 'checked_out', 'checkout_time', 'checked_out_by']
    
admin.site.register(HospiTeam, HospiTeamAdmin)
admin.site.register(Hostel)
admin.site.register(Room)
admin.site.register(Allotment, AllotmentAdmin)
admin.site.register(HospiLog, HospiLogAdmin)
