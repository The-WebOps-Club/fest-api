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
from apps.walls.models import Wall, Post
# Forms
from forms import LoginForm, ProfileForm, UserForm
# View functions
# Misc
from django.templatetags.static import static
from misc import strings
# Python
import os

def login_user(request):
    """ 
        A view is to handle the baisc login methods in ERP

        Args:
            request:   The HTTP Request

        Kwargs:
            kwargs**:  None

        Returns:
            IF login was successful : redirects to `home.views.home()`
            
            ELSE : renders the `pages/login.html`
            > Context variables in the `pages/login.html` :-
                - global_context_variables : misc.utils.global_context()
                - login_form : `users.forms.LoginForm`
    
        Raises:
            None

        Daemon Tasks:
            - Sets various django.contrib.messages depending on actions takes in the view
            - Authenticates and logs in a django.contrib.auth.User

    """
    login_form = LoginForm()
    if request.method == "POST":
        print "post"
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # Checks for username and password
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            # Authenticates user against database
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user) # Logs in the User
                    return redirect("apps.home.views.home") # Redirect to home page
                else:
                    messages.error(request, strings.LOGIN_ERROR_INACTIVE)
            else:
                messages.error(request, strings.LOGIN_ERROR_INACTIVE)
        else:
            messages.error(request, strings.LOGIN_ERROR_INVALID)
    local_context = {
        "login_form" : login_form,
    }
    return render_to_response("pages/login.html", local_context, context_instance= global_context(request))

def profile(request, id=None):
    """ 
        A view to handle the profile page about a user showing various information about the user.
        It can also be for a department or subdepartment

        Args:
            request:   The HTTP Request
            id:        The id who's profile should be shown

        Kwargs:
            kwargs**:  None

        Returns:
            IF id found in database : renders `pages/profile.html`
            > Context variables in the `pages/profile.html` :-
                - global_context_variables : misc.utils.global_context()
                - profile_form : `users.forms.ProfileForm`
    
        Raises:
            None

        Daemon Tasks:
            - Sets various django.contrib.messages depending on actions takes in the view
            - Saves edited Profile information             
    """
    if not id:
        id = request.user.id
    user = get_object_or_404(User, pk=id)
    profile = ERPUser.objects.get(user=user)
    try:
        profile = ERPUser.objects.get(user=user)
    except ERPUser.DoesNotExist:
        profile = ERPUser.objects.create(user=user)
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
    local_context = {
        "profile_form" : profile_form,
    }
    return render_to_response("pages/profile.html", local_context, context_instance= global_context(request))

def temp_profile(request):
    erp_profile_form = ProfileForm()
    user_form = UserForm()
    profile_form = UserForm()
    local_context = {
        "profile_form" : profile_form,
    }
    return render_to_response("pages/profile.html", locals(), context_instance= global_context(request))