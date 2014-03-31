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
from apps.walls.models import Post, Comment
from notifications.models import Notification
# Forms
# View functions
# Misc
from django.templatetags.static import static
# Python
import os

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
    local_context = {
    	"current_page" : "newsfeed",
    	"notifications" : Notification.objects.order_by("-timestamp"),
    }
    return render_to_response("pages/newsfeed.html", local_context, context_instance= global_context(request))

@login_required
def portals(request):
    # notifications = request.user.notifications.unread()
    # print notifs
    return render_to_response("pages/portals.html", locals(), context_instance= global_context(request))

@login_required
def notifications(request):
    local_context = {
    	"current_page" : "newsfeed",
    	#"posts" : Post.objects.order_by("-comments__time_updated", "-time_updated"),
    	"notifications" : request.user.notifications.unread(),
    }
    return render_to_response("pages/newsfeed.html", locals(), context_instance= global_context(request))


@login_required
def contacts(request):
    return render_to_response("pages/notifications.html", locals(), context_instance= global_context(request))

# Gen for testing purposes
@login_required
def show_newsfeed(request):
    return render_to_response("pages/newsfeed.html", locals(), context_instance= global_context(request))
        