from django import forms
from apps.users.models import UserProfile
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

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        #exclude = ['dob','last_login', 'saarang_id', 'friend_list', 'fb_token', 'activate_status', 'fb_id', 'accomod_is_confirmed', 'password', 'college_id_hospi']
        fields = [
            'user',
            'desk_id',
            'gender',
            'mobile_number',
            'college_text',
            'college_roll',
        ]