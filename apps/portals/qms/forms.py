from django import forms
from django.db import models
from apps.users.models import UserProfile, Team
from apps.events.models import EventRegistration
from django.contrib.auth.models import User


class AddUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','password','first_name', 'last_name','email']
      
     
class AddTeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name','members','accomodation_status']
        
class UserProfileForm(forms.ModelForm):
	dob = forms.DateField(label=u'Date of Birth', input_formats=['%d/%m/%Y', '%d-%m-%Y', '%d %b, %Y', '%B %d, %Y'], required=False, widget=forms.DateInput(format = '%d %b, %Y'))
    
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
			'city',
			'want_accomodation',
			'saarang_id',
			'desk_id',
			'fb_id',
			'college_id_hospi',
			'accomod_is_confirmed',
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



class AddEventRegistrationForm(forms.ModelForm):
    class Meta:
        model = EventRegistration
        #fields = ['name','members','accomodation_status']
