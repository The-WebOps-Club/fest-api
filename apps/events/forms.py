from django import forms
from apps.events.models import EventTab

class AddEventTabForm(forms.ModelForm):
    class Meta:
        model = EventTab
        fields = ('name','content')
