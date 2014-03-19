# Django
from django.shortcuts import render_to_response, redirect, HttpResponseRedirect, render
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.conf import settings
# Apps
from misc.utils import *  #Import miscellaneous functions
# Decorators
# Models
from django.contrib.auth.models import User
# Forms
from forms import LoginForm
# View functions
# Misc
from django.templatetags.static import static
# Python
import os

def login_user(request):
    """ Renders login view process POST logs into home page """
    loginform = LoginForm()
    if request.method == "POST":
        print 'post'
        loginform = LoginForm(request.POST)
        if loginform.is_valid():
            # Checks for username and password
            username = loginform.cleaned_data['username']
            password = loginform.cleaned_data['password']
            # Authenticates user against database
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user) # Logs in the User
                    return redirect('apps.home.views.home') # Redirect to home page
                else:
                    messages.error(request, "Account not active")
            else:
                messages.error(request, "Incorrect username or password")
        else:
            print "Didnt validate"
    return render_to_response('pages/login.html', locals(), context_instance= global_context(request))

def profile(request):
    """ Lets the user ot view and edit profile """
