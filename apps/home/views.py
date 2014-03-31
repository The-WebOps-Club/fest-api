# Django
from django.shortcuts import render_to_response, redirect, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
# Apps
from misc.utils import *  #Import miscellaneous functions
# Decorators
# Models
from django.contrib.auth.models import User
# Forms
# View functions
# Misc
from django.templatetags.static import static
# Python
import os
import notifications 

@login_required
def home (request, *args, **kwargs):
	"""
		The home page that people will see when the login or go to the root URL
		 - Redirects to newsfeed if logged in
		 - Redirects to login page if not logged in
	"""
	return redirect("apps.home.views.newsfeed")
    

@login_required
def newsfeed(request):
    # notifications = request.user.notifications.unread()
    # print notifs
    return render_to_response("pages/newsfeed.html", locals(), context_instance= global_context(request))

@login_required
def portals(request):
    # notifications = request.user.notifications.unread()
    # print notifs
    return render_to_response("pages/portals.html", locals(), context_instance= global_context(request))

@login_required
def notifications(request):
    # notifications = request.user.notifications.unread()
    # print notifs
    return render_to_response("pages/notifications.html", locals(), context_instance= global_context(request))

# Gen for testing purposes
@login_required
def show_newsfeed(request):
    return render_to_response("pages/newsfeed.html", locals(), context_instance= global_context(request))
        