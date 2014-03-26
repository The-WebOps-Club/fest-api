from django import forms
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User
from models import ERPProfile

class LoginForm(forms.Form):
    """
		The form which will show basic requirements ot login using suername & password

		Fields:
			username: 	The username of the user trying to login. django.contrib.auth.models.User.username
			password: 	The password of the user trying to login. django.contrib.auth.models.password unhashed

	"""
    
    username = forms.CharField(required=True, widget=forms.TextInput( attrs= {
				'required' : 'true',
			}
		)
   	)
    password = forms.CharField(required=True, 
    	widget=forms.PasswordInput(
    		attrs = {
    			'required' :'true',
    		}
    	)
    )

class UserForm(forms.ModelForm):
    """
		The form which will shows django.contrin.auth.models.User

		Fields:
			first_name: The first_name of the user from django.contrib.auth.models.User
			last_name:  The last_name of the user from django.contrib.auth.models.User
			email:  	The last_name of the user from django.contrib.auth.models.User
			password: 	The password of the user trying to login. django.contrib.auth.models.password unhashed
	"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password' ]

class ProfileForm(forms.ModelForm):
    class Meta:
        model = ERPProfile
        exclude = ('user', 
            'wall',
            'coord_relations', 
            'supercoord_relations', 
            'core_relations',
        )
