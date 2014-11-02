
from django.contrib import admin

from apps.events.models import Tab

from apps.events.models import EventRegistration

#admin.site.register(Event)
admin.site.register(Tab)

#new
#admin.site.register(EventTab)
admin.site.register(EventRegistration)
