
from django.contrib import admin

from apps.portals.events.models import Event, Tab

from apps.portals.events.models import EventTab

admin.site.register(Event)
admin.site.register(Tab)

#new
admin.site.register(EventTab)