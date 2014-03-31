# Django
from django.shortcuts import get_object_or_404, render_to_response, redirect, HttpResponseRedirect, render
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.templatetags.static import static
# Apps
from misc.utils import *  #Import miscellaneous functions
from misc import strings
# Decorators
# Models
from django.contrib.auth.models import User
from apps.users.models import ERPProfile, UserProfile, Dept, Subdept
from apps.walls.models import Wall, Post
# Forms
from forms import LoginForm, ProfileForm, UserForm
# View functions
# Misc
from annoying.functions import get_object_or_None
# Python
import os

def login_user(request):
    """ 
        A view to handle the baisc login methods in ERP

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
    current_page = "profile"# Default argument setting and checking
    if request.user.is_authenticated(): # Check if user is already logged in
        return redirect("apps.home.views.home")

    # Logic
    login_form = LoginForm()
    # POST Logic
    print request.method
    if request.method == "POST": # Check if POST data is there for the LoginForm
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
                    #print "Logged the user in successfully"
                    return HttpResponseRedirect(reverse("identity")) # Redirect to home page
                else:
                    login_form.errors.update( {
                        "submit" : "The user has been deactivated.",
                    } )
                
            else: # errors appeared
                login_form.errors.update( {
                    "submit" : "The username or password is incorrect",
                } )
                messages.error(request, strings.LOGIN_ERROR_INACTIVE)
        else:
            print dict(login_form.errors)
            pass
    # import pdb; pdb.set_trace()
    # Return
    local_context = {
        "current_page" : "login",
        "login_form": login_form,
    }
    return render_to_response("pages/login.html", local_context, context_instance= global_context(request))

@login_required
def profile(request, user_id=None):
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
            ERPProfile.DoesNotExist, 

        Daemon Tasks:
            - Sets various django.contrib.messages depending on actions takes in the view
            - Saves edited Profile information             
    """
    # Default argument setting and checking
    if user_id == None or user_id == request.user.id:
        user_id = request.user.id
        user = request.user
    else:
        user = get_object_or_404(User, pk=user_id)

    # Lofic of the view
    erp_profile = user.erp_profile
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
    # Return
    local_context = {
        "current_page" : "profile",
        "profile_form" : profile_form,
    }
    return render_to_response("pages/profile.html", local_context, context_instance= global_context(request))

@login_required

def identity(request, role_type=None, role_id=None):
    """
        Changes identity of the user based on the arguments

        Args:
            role_type: An element from the set ("coord", "supercoord", "core") defining the role in fest
            rold_id: The ID of the relation to the corresponding subdept (in case of coord) or Dept (for supercoord/core)

        Kwargs:
            kwargs**:  None

        Returns:
            IF no args:
                Finds highest position the person is eligible for and sets first department in that
            ELSE:
                Alots the corresponding position mentioned in the arguments. 
                If the position does not exist. It raises an error
        Raises:
            Dept.DoesNotExist, Subdept.DoesNotExist

        Daemon Tasks:
            - Sets various request.sessions
    """
    # Default argument setting and checking
    if role_type == None and role_id == None:
    	if not hasattr(request.session, "role"): # Do only if no role has been set yet
		    if request.user.erp_profile.core_relations.count():
		        role_type = "core"
		        role_id = request.user.erp_profile.core_relations.first().id
		    elif request.user.erp_profile.supercoord_relations.count():
		        role_type = "supercoord"
		        role_id = request.user.erp_profile.supercoord_relations.first().id
		    elif request.user.erp_profile.coord_relations.count():
		        role_type = "coord"
		        role_id = request.user.erp_profile.coord_relations.first().id
    else:
        # Initial validations
        try:
            role_id = int(role_id)
        except ValueError:
            print role_id, "could not convert to int"
            role_id = None
        if not ( type(role_type) is str or type(role_type) is unicode ) or type(role_id) is not int:
            print role_id, type(role_id)
            print role_type, type(role_type)
            raise InvalidArgumentTypeException
        if ( role_type == "coord" and get_object_or_None(Subdept, id=role_id) == None ) or \
            ( ( role_type == "supercoord" or role_type == "core" ) and get_object_or_None(Dept, id=role_id) == None ):
            raise InvalidArgumentValueException


    # Logic of the view
    request.session["role"] = role_type
    request.session["role_dept"] = int(role_id)

    if role_type == "core":
        request.session["is_core"] = True
        request.session["is_supercoord"] = False
        request.session["is_coord"] = False
    elif role_type == "supercoord":
        request.session["is_core"] = False
        request.session["is_supercoord"] = True
        request.session["is_coord"] = False
    elif role_type == "coord":    
        request.session["is_core"] = False
        request.session["is_supercoord"] = False
        request.session["is_coord"] = True

    # Return
    return redirect("apps.home.views.home")

def show_profile(request):
    erp_profile_form = ProfileForm()
    user_form = UserForm()
    profile_form = UserForm()
    local_context = {
        "profile_form": profile_form,
        "erp_profile_form": erp_profile_form,
        "user_form": user_form,
    }
    return render_to_response("pages/profile.html", locals(), context_instance= global_context(request))

def show_login_user(request):
    login_form = LoginForm()
    local_context = {
        "login_form" : login_form,
    }
    return render_to_response('pages/wall.html', locals(), context_instance= global_context(request))
