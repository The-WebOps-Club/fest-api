from django import forms
from apps.users.models import UserProfile
from models import Hostel, Room, HospiTeam
from misc.constants import *

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


class UserProfileForm(forms.Form):
    first_name         = forms.CharField(max_length=30)
    last_name          = forms.CharField(max_length=30)
    email              = forms.EmailField(max_length=100)
    dob                = forms.DateField(label=u'Date of Birth', input_formats=['%d/%m/%Y', '%d-%m-%Y', '%d %b, %Y', '%B %d, %Y'], required=False, widget=forms.DateInput(format = '%d %b, %Y'))
    gender             = forms.ChoiceField(choices=GENDER_CHOICES)
    mobile_number      = forms.CharField(max_length=15, help_text='Please enter your current mobile number')
    branch             = forms.ChoiceField(choices=BRANCH_CHOICES, help_text='Your branch of study')
    college_text       = forms.CharField(max_length=50)
    college_roll       = forms.CharField(max_length=40)
    '''
    class Meta:
        model = UserProfile
        fields = [
            'gender', 
            'dob', 
            'mobile_number',
            'branch',
            'college',
            'college_roll',
            'school_student',
            'want_accomodation',
        ]

    def init(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['dob'].input_formats = settings.DATE_INPUT_FORMATS

    # def clean_dob(self):
        
    def save(self, commit=True, *args, **kwargs):
        instance = super(UserProfileForm, self).save(commit=False, *args, **kwargs)
        if commit:
            instance.save()
        return instance
    '''