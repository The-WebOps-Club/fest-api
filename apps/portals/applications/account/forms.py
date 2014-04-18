#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
from django import forms
from django.forms.util import ValidationError
from django.contrib.auth.models import User
from apps.portals.applications.account.models import UserProfile

alnum_re    = re.compile(r'^[\w.-]+$')  # regexp. from jamesodo in #django  [a-zA-Z0-9_.]
alphanumric = re.compile(r"[a-zA-Z0-9]+$")


class LoginForm(forms.Form):
    """
        This form is used for login
    """
    username = forms.CharField(help_text = 'Your registered Roll No')
    password = forms.CharField(widget    = forms.PasswordInput, help_text='Your password')

class EditUserProfileForm(forms.ModelForm):
    """
        This model form is for Editting User Profile details
    """
    first_name     = forms.CharField(max_length = 30)
    last_name      = forms.CharField(max_length = 30)
    
    class Meta:
        model = UserProfile
        exclude = ('user', 'is_core_of', )    

    def clean_first_name(self):
        """
            This function validates the first name of the user to ensure it contains only letters.
        """
        if not self.cleaned_data['first_name'].replace(' ', '').isalpha():
            raise forms.ValidationError('Names cannot contain anything other than alphabets.')
        else:
            return self.cleaned_data['first_name']

    def clean_last_name(self):
        """
            This function validates the last name of the user to ensure it contains only letters.
        """
        if not self.cleaned_data['last_name'].replace(' ', '').isalpha():
            raise forms.ValidationError('Names cannot contain anything other than alphabets.')
        else:
            return self.cleaned_data['last_name']

class RegistrationForm(EditUserProfileForm):
    """
        This model form is used registration by the aspiring coordinators
    """
    rollno         = forms.CharField(max_length = 8, help_text='Please enter your Roll No.', label='Roll Number')
    email          = forms.EmailField()
    password       = forms.CharField(min_length = 6, max_length = 30, widget = forms.PasswordInput, help_text = 'Passwords need to be atleast 6 characters long.')
    password_again = forms.CharField(min_length = 6, max_length = 30, widget = forms.PasswordInput, help_text = 'Enter the same password that you entered above')
        
    def clean_rollno(self):
        """
            This function validates the Roll Number field using RegEx expression
        """
        if not alphanumric.search(self.cleaned_data['rollno']):
            raise forms.ValidationError(u'Roll No can only contain letters and numbers')
        if User.objects.filter(username = self.cleaned_data['rollno']):
            pass
        else:
            return self.cleaned_data['rollno']
        raise forms.ValidationError('This username is already taken. Please choose another.')

    def clean_email(self):
        """
            This functions validates the entered email id to ensure the email id hasn't been used
            earlier for another registration
        """
        if User.objects.filter(email = self.cleaned_data['email']):
            pass
        else:
            return self.cleaned_data['email']
        raise forms.ValidationError('This email address is already taken. Please choose another.')

    def clean_password(self):
        """
            This function validates the password field to check if the entered passwords match.
        """
        if self.prefix:
            field_name1 = '%s-password' % self.prefix
            field_name2 = '%s-password_again' % self.prefix
        else:
            field_name1 = 'password'
            field_name2 = 'password_again'

        if self.data[field_name1] != '' and self.data[field_name1] != self.data[field_name2]:
            raise forms.ValidationError('The entered passwords do not match.')
        else:
            return self.data[field_name1]
            
    def clean_ph_no(self):
        """
            This function validates the entered phone number. Only a 10 digit number is accepted.
            The function also ensures the number isn't already registered.
        """
        if len(self.cleaned_data['ph_no']) != 10 or not self.cleaned_data['ph_no'].isdigit():
            raise forms.ValidationError('Enter a valid 10 digit mobile number')
        if UserProfile.objects.filter(ph_no = self.cleaned_data['ph_no']):
            pass
        else:
            return self.cleaned_data['ph_no']
        raise forms.ValidationError('This mobile number is already registered')

