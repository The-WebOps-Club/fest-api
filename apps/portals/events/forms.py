from django import forms
from django.db import models
from apps.events.models import Event, EventSchedule, EventWinner
from apps.users.models import ERPProfile
import select2.fields

class AddEventForm(forms.ModelForm):
    COORDS = [[coord.id, coord.name] for coord in ERPProfile.objects.all()]
    coords = forms.MultipleChoiceField(choices=COORDS, required=False)
    coords.widget.attrs.update({'placeholder': 'Select coordinators', 'style':'width:300px'})
    class Meta:
        model = Event
        fields=('name','is_visible','short_description','event_type','category','has_tdp','team_size_min','team_size_max','registration_starts','registration_ends','coords','google_group','email','google_form','long_description','extra_info',)

class ImageEventForm(forms.Form):
	event_id = forms.IntegerField(required=True)
	image = forms.ImageField(required=True) 

class AddSlotForm(forms.ModelForm):
	class Meta:
		model = EventSchedule

class EventWinnerForm(forms.ModelForm):
    class Meta:
        model=EventWinner
        fields=('event','position','comment','user')