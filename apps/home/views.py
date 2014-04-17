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
    user = request.user
    
    if settings.SOCIAL_AUTH_FORCE_FB and user.social_auth.filter(provider="facebook").count() == 0:
        return redirect("apps.users.views.associate")

    if user.is_authenticated(): # Check if user is already logged in
        if "role" not in request.session.keys():
            return HttpResponseRedirect(reverse("identity")) # Redirect to home page

    return redirect("apps.home.views.newsfeed")
    

@login_required
def newsfeed(request): 
    user = request.user
    local_context = {
        "current_page" : "newsfeed",
        "notifications" : Notification.objects.order_by("-timestamp")[:5],
    }
    return render_to_response("pages/newsfeed.html", local_context, context_instance= global_context(request))

@login_required
def portals(request):
    # notifications = request.user.notifications.unread()
    # print notifs
    local_context = {}
    return render_to_response("pages/portals.html", local_context, context_instance= global_context(request))

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
    notif.public = False #Use this to check if a notification was "read" by recipient, or another notif was added for same post
    notif.save()
    notif.mark_as_read()
    return redirect(reverse("wall", kwargs={ "wall_id" : notif.target.wall.id }) + "#post_" + str(notif.target.id))

@login_required
def contacts(request):
    local_context = {
    }
    return render_to_response("pages/contacts.html", local_context, context_instance= global_context(request))

@login_required
def markdown(request):
    local_context={}
    return render_to_response("pages/markdown.html", local_context, context_instance= global_context(request))
