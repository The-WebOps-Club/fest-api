from django import forms
from apps.events.models import EventTab, Event

class AddEventTabForm(forms.ModelForm):
    class Meta:
        model = EventTab
        fields = ('name','content')

class AddEventForm(forms.ModelForm):
    class Meta:
        model = Event
        