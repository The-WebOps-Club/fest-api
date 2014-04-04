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
    	"current_page" : "notifications",
    	#"posts" : Post.objects.order_by("-comments__time_updated", "-time_updated"),
    	"notifications" : request.user.notifications.all(),
    }
    return render_to_response("pages/newsfeed.html", local_context, context_instance= global_context(request))

@login_required
def read_notification(request, notif_id):
	if notif_id == "all":
		request.user.notifications.mark_all_as_read()
		return redirect(reverse("newsfeed"))
	else:
		try:
			notif_id = int(notif_id)
		except ValueError:
			print notif_id, "could not convert to int"
			notif_id = None
		if not ( type(notif_id) is int ):
			print "notif_id :", notif_id, type(wall_id)
			raise InvalidArgumentTypeException
		try:
			notif = request.user.notifications.get(id = notif_id)
		except Notification.DoesNotExist:
			raise InvalidArgumentValueException
	# Logic
	notif.mark_as_read()
	return redirect(reverse("wall", kwargs={ "wall_id" : notif.target.wall.id }) + "#post_" + str(notif.target.id))


@login_required
def contacts(request):
    return render_to_response("pages/notifications.html", locals(), context_instance= global_context(request))

@login_required
def markdown(request):
    return render_to_response("pages/markdown.html", locals(), context_instance= global_context(request))

# Gen for testing purposes
@login_required
def show_newsfeed(request):
    return render_to_response("pages/newsfeed.html", locals(), context_instance= global_context(request))
        