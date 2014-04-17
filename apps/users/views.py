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
from misc.constants import HOSTEL_CHOICES, BRANCH_CHOICES
# Decorators
# Models
from django.contrib.auth.models import User
from apps.users.models import ERPProfile, UserProfile, Dept, Subdept
from apps.walls.models import Wall, Post
# Forms
from forms import LoginForm, UserProfileForm, ERPProfileForm, UserForm
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
        if hasattr(request.session, "role"):
            return redirect("apps.home.views.home")
        else:
            return HttpResponseRedirect(reverse("identity")) # Redirect to home page

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
                    if ( not hasattr(user, "erp_profile") ): # No erp_profile ! Ask them to fill up forms
                        return HttpResponseRedirect(reverse("profile")) # Redirect to home page    
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
def associate(request): 
    user = request.user
    local_context = {
        "current_page" : "associate",
        "facebook_association" : user.social_auth.filter(provider="facebook").count(),
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
        read_only = False
    else:
        user = get_object_or_404(User, pk=user_id)
        read_only = True

    # Lofic of the view
        # Basic variables
    erp_profile = None
    user_profile = None
    if hasattr(user, "erp_profile"):
        erp_profile = user.erp_profile
    if hasattr(user, "profile"):
        user_profile = user.profile
    user_form = UserForm(instance = user)
    user_profile_form = UserProfileForm(instance=user_profile)
    erp_profile_form = ERPProfileForm(instance=erp_profile)
    
    data = request.POST.copy()
    if request.method == "POST":
        hostel_name = data.get("hostel", None)
        if hostel_name: data["hostel"] = data["hostel"].strip()
        branch_name = data.get("branch", None)
        if branch_name: data["branch"] = data["branch"].strip()
        summer_stay_data = data.getlist("summer_stay", None)
        if summer_stay_data: data["summer_stay"] = " and ".join([i.strip() for i in data.getlist("summer_stay")])
        print summer_stay_data
        print data['summer_stay']
        # winter_stay_data = data.get("winter_stay", None)
        # if winter_stay_data: data["winter_stay"] = " and ".join([i.strip() for i in data.getlist("winter_stay")])
        # print winter_stay_data
        print "----------------------------------------"
        print ">>>>>>>>>", data
        user_form = UserForm(data, instance = user)
        user_profile_form = UserProfileForm(data, instance=user_profile)
        erp_profile_form = ERPProfileForm(data, instance=erp_profile)
        
        user_form_is_valid = user_form.is_valid()
        user_profile_form_is_valid = user_profile_form.is_valid()
        erp_profile_form_is_valid = erp_profile_form.is_valid()
        if user_form_is_valid:
            user = user_form.save(commit=False)
        if user_profile_form_is_valid:
            user_profile = user_profile_form.save(commit=False)
        if erp_profile_form_is_valid:
            erp_profile = erp_profile_form.save(commit=False)
        
        if user_form_is_valid and user_profile_form_is_valid and erp_profile_form_is_valid:
            user.save()    
            user_profile.save()    
            erp_profile.save()    
        else:
            # print user_form.errors
            # print user_profile_form.errors
            # print erp_profile_form.errors
            pass
    
    print [unicode(i) for i in user_profile_form.fields['dob'].input_formats]
    # Return
    local_context = {
        "current_page" : "profile",
        "user_form" : user_form,
        "user_profile_form" : user_profile_form,
        "erp_profile_form" : erp_profile_form,
        "profile_wall" : erp_profile.wall,
        "read_only" : read_only,
        "HOSTEL_CHOICES" : [i[0] for i in HOSTEL_CHOICES],
        "BRANCH_CHOICES" : [i[0] for i in BRANCH_CHOICES],
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

# --------------------------------------------------------------
# Views for Python Social auth
