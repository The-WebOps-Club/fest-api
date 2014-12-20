from django import forms
from django.db import models
from apps.users.models import UserProfile, Team
from django.contrib.auth.models import User


class AddUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','password','first_name', 'last_name','email']

