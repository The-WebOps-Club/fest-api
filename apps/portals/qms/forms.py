from django import forms
from django.db import models
from apps.users.models import UserProfile, Team


class AddUserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile

