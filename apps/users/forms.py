from django import forms
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User
from apps.users.models import ERPProfile, UserProfile, Dept, Subdept

class LoginForm(forms.Form):
	"""
		The form which will show basic requirements ot login using suername & password

		Fields:
			username: 	The username of the user trying to login. django.contrib.auth.models.User.username
			password: 	The password of the user trying to login. django.contrib.auth.models.password unhashed

	"""
	
	username = forms.CharField(required=True, widget=forms.TextInput( 
			attrs= {
				'required' : 'true',
			}
		)
	)
	password = forms.CharField(required=True, widget=forms.PasswordInput(
			attrs = {
				'required' :'true',
			}
		)
	)

class UserForm(forms.ModelForm):
	"""
		The form which will show django.contrin.auth.models.User fields and handle it's field validation

		Fields:
			first_name: The first_name of the user from django.contrib.auth.models.User
			last_name:  The last_name of the user from django.contrib.auth.models.User
			email:  	The last_name of the user from django.contrib.auth.models.User
	"""
	class Meta:
		model = User
		fields = [
			'first_name', 
			'last_name', 
			'email'
		]

	def save(self, commit=True, *args, **kwargs):
		instance = super(UserForm, self).save(commit=False, *args, **kwargs)
		
		if commit:
			instance.save()
		return instance

class UserProfileForm(forms.ModelForm):
	"""
		The form which will show apps.users.models import UserProfile's fields and handle authentication

		Fields:
			
	"""
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

class ERPProfileForm(forms.ModelForm):
	"""
		The form which will show apps.users.models.ERPProfile's fields and handle validations

		Fields:
			
	"""
	class Meta:
		model = ERPProfile
		fields = [
			'nickname',
			'room_no',
			'hostel',
			'summer_number',
			'summer_stay',
			'summer_stay2',
			'winter_stay',
			'winter_stay2',
		]

	def save(self, commit=True, *args, **kwargs):
		instance = super(ERPProfileForm, self).save(commit=False, *args, **kwargs)
		if commit:
			instance.save()
		return instance






