from django import forms
from apps.portals.events.models import Event


class AddEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields=('name','short_description','event_type','category','has_tdp','team_size_min','team_size_max','registration_starts','registration_ends','google_group','email')
