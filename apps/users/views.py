# Django
from django.shortcuts import get_object_or_404, render_to_response, redirect, HttpResponseRedirect, render
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
# Apps
from misc.utils import *  #Import miscellaneous functions
# Decorators
# Models
from django.contrib.auth.models import User
from models import ERPUser
from apps.walls.models import Wall
# Forms
from forms import LoginForm, ProfileForm, UserForm
# View functions
# Misc
from django.templatetags.static import static
from misc import strings
# Python
import os

def login_user(request):
    """ Renders login view process POST logs into home page """
    if request.method == "POST":
        data=request.POST.copy()
        # Checks for username and password
        username = data["username"]
        password = data["password"]
        # Authenticates user against database
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user) # Logs in the User
                return redirect("apps.home.views.home") # Redirect to home page
            else:
                messages.error(request, strings.LOGIN_ERROR_INACTIVE)
        else:
            messages.error(request, strings.LOGIN_ERROR_WRONG_CRED)
    return render_to_response("pages/login.html", locals(), context_instance= global_context(request))

@login_required
def profile(request):
    """ 
        Lets the user view and edit profile
        Creates an new profile if one does not exist
    """
    user = get_object_or_404(User, pk=request.user.pk)
    profile = ERPUser.objects.get(user=user)
    try:
        profile = ERPUser.objects.get(user=user)
    except ERPUser.DoesNotExist:
        new_wall = Wall.objects.create(name=user.username)
        new_user = ERPUser.objects.create(user=user, wall=new_wall)
    form = UserForm(instance = user)
    profile_form = ProfileForm(instance=profile)
    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            profile_form = ProfileForm(request.POST, instance=profile)
            if profile_form.is_valid():
                user.save()
                profile_form.save()
                messages.success(request, strings.UPDATE_SUCCESS %("Profile"))
            else:
                messages.error(request, strings.INVALID_FORM)
        else:
            messages.error(request, strings.INVALID_FORM)
    return render_to_response("pages/profile.html", locals(), context_instance= global_context(request))

def newsfeed(request):
    newsfeed = True
    return render_to_response("pages/newsfeed.html", locals(), context_instance= global_context(request))