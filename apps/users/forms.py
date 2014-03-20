from django import forms
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User
from models import ERPUser

class LoginForm(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'required':'true'}))
    password = forms.CharField(required=True,widget=forms.PasswordInput(attrs={'required':'true'}))

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email' ]

class ProfileForm(forms.ModelForm):
    class Meta:
        model = ERPUser
        exclude = ('user', 'wall','coord_relations', 'supercoord_relations', 'core_relations')
