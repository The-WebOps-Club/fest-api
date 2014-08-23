
from django.contrib import admin

from apps.events.models import Event, Tab

from apps.events.models import EventTab

admin.site.register(Event)
admin.site.register(Tab)

#new
admin.site.register(EventTab)