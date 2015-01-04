from django import forms
from django.db import models
from apps.users.models import UserProfile, Team
from apps.events.models import EventRegistration,EventParticipation
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
	class Meta:
		model = UserProfile
		fields = [
			'gender',  
			'age', 
			'mobile_number',
			'branch',
			'college_text',
			'city',
			'desk_id',
		]
		
	def save(self, commit=True, *args, **kwargs):
		instance = super(UserProfileForm, self).save(commit=False, *args, **kwargs)
		if commit:
			instance.save()
		return instance



class AddEventRegistrationForm(forms.ModelForm):
    class Meta:
        model = EventRegistration
        #fields = ['name','members','accomodation_status']
        
        
class EventParticipationForm(forms.ModelForm):
    class Meta:
        model = EventParticipation
