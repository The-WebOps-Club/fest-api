from django import forms

from models import Hostel, Room, HospiTeam

class HostelForm(forms.ModelForm):
    class Meta:
        model = Hostel

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        exclude = ['occupants']

class HospiTeamForm(forms.ModelForm):
    class Meta:
        model = HospiTeam
        exclude = ['team_sid', 'members', 'checked_in', 'checked_out', 'mattress_count', 'mattress_returned' ]
    def __init__(self, *args, **kwargs):
        super(HospiTeamForm, self).__init__(*args, **kwargs)
        self.fields['leader'].widget.attrs['id'] = "multiselect1"
        self.fields['leader'].widget.attrs['style'] = "width: 220px;"
