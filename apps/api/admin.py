
from django.contrib import admin

from apps.api.models import PushNotification, BandHuntTrack, BandHuntVote

admin.site.register(PushNotification)
admin.site.register(BandHuntTrack)
admin.site.register(BandHuntVote)
