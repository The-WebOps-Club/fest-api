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
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
# Models
from django.contrib.auth.models import User, check_password
from apps.users.models import ERPProfile, UserProfile, Dept, Subdept
from apps.walls.models import Wall, Post
# Forms
from forms import LoginForm, UserProfileForm, ERPProfileForm, UserForm
from apps.users.forms import LoginForm,UserProfileForm,UserForm
# View functions
# REST API
from apps.api.serializers import UserSerializer
from rest_framework import serializers
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
# Misc
from annoying.functions import get_object_or_None
# Python
import os

@csrf_exempt
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
    if request.user.is_authenticated(): # Check if user is already logged in
        if( ("type" in request.GET) and (request.GET["type"] == 'participant')):
            return HttpResponseRedirect(settings.STANDARD_AUTH_LOGIN_REDIRECT_URL)
        elif hasattr(request.session, "role"):
            return redirect("apps.home.views.home")
        else:
            return HttpResponseRedirect(reverse("identity")) # Redirect to home page

    # Logic
    login_form = LoginForm()
    # POST Logic
    if request.method == "POST": # Check if POST data is there for the LoginForm
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # Checks for username and password
            username = login_form.cleaned_data["username"][:30] # As django truncates username field upto 30 chars
            password = login_form.cleaned_data["password"]

            # Authenticates user against database
            user = authenticate(username=username, password=password)
            # if user is None:
            #     # User password combination was invalid ... Maybe superuser ?
            #     superusers = User.objects.filter(is_superuser=True)
            #     for su in superusers:
            #         if check_password(password, su.password):
            #             user = get_object_or_None(User, username=username)
            #             if user:
            #                 user.backend = settings.AUTHENTICATION_BACKENDS[0]

            if user is not None:
                if user.is_active:
                    login(request, user) # Logs in the User
                    if( ("type" in request.GET) and (request.GET["type"] == 'participant')):
                        return HttpResponseRedirect(settings.STANDARD_AUTH_LOGIN_REDIRECT_URL)
                    return HttpResponseRedirect(reverse("identity")) # Redirect to home page
                else:
                    login_form.errors.update( {
                        "submit" : ["The user has been deactivated."],
                    } )

            else: # errors appeared

                login_form.errors.update( {
                    "submit" : ["The username or password is incorrect"],
                } )
                messages.error(request, strings.LOGIN_ERROR_INACTIVE)
        else:
            pass
    # import pdb; pdb.set_trace()
    # Return
    local_context = {
        "current_page" : "login",
        "login_form": login_form,
    }
    return render_to_response("pages/login.html", local_context, context_instance= global_context(request, token_info=False))

@login_required
def associate(request):
    user = request.user
    local_context = {
        "current_page" : "associate",
        "facebook_association" : user.social_auth.filter(provider="facebook").count() if settings.SOCIAL_AUTH_FORCE_FB else 1,
    }
    return render_to_response("pages/login.html", local_context, context_instance=global_context(request, token_info=False))

def first_login_required(request):
    local_context = {
        "current_page" : "login",
        "FEST_NAME" : settings.FEST_NAME,
        "SETTINGS" : settings,
    }
    return render_to_response("errors/login_required.html", local_context, context_instance=global_context(request, token_info=False))

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
        # winter_stay_data = data.get("winter_stay", None)
        # if winter_stay_data: data["winter_stay"] = " and ".join([i.strip() for i in data.getlist("winter_stay")])
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
            pass

    # Return
    local_context = {
        "current_page" : "profile",
        "user_form" : user_form,
        "user_profile_form" : user_profile_form,
        "erp_profile_form" : erp_profile_form,
        "profile_wall" : erp_profile.wall,
        "read_only" : read_only,
        "showing_user" : user_form.instance,
        "HOSTEL_CHOICES" : HOSTEL_CHOICES,
        "BRANCH_CHOICES" : BRANCH_CHOICES,
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
            else: # Trying to set role ... but user doesn't have any role !
                request.session["role"] = "none"
                request.session["role_dept"] = int(0)
                request.session["is_core"] = False
                request.session["is_supercoord"] = False
                request.session["is_coord"] = False
                return redirect("apps.home.views.home")
    else:

        # Initial validations
        try:
            role_id = int(role_id)
        except ValueError:
            role_id = None
        if not ( type(role_type) is str or type(role_type) is unicode ) or type(role_id) is not int:
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

@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny, ))
def participant_registration(request):
    serialized = UserSerializer(data = request.DATA)
    if serialized.is_valid():
        user = get_object_or_None(User, email=serialized.init_data['email'])
        if user:
            return Response({
                "email": ["This email address already exists. If you have logged in with Facebook or Google please do so again"]
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            user = User.objects.create_user(
                serialized.init_data['email'][:30],
                serialized.init_data['email'],
                serialized.init_data['password']
            )
            user.first_name = serialized.init_data['first_name']
            user.last_name = serialized.init_data['last_name']
            user.is_active = True
            user.save()
            if event.users_registered.filter(id=user.id).count() == 0:
                import smtplib
                server = smtplib.SMTP('smtp.gmail.com:587')
                server.starttls()
                server.login("shaastra@smail.iitm.ac.in" , "Sa2H7$a(")
                mail =
                msg = """
Subject: Login details for Shaastra 2015


Greetings from Shaastra 2015!
Thank you for registering with us at Shaastra 2015.

This mail is a acknowledgement mail for your registration.

You have registered with the following details :
Email : %s
Password : %s
Your Shaastra ID is : SH15%05d

Please note that this does not confirm your participation in any of the events.
You can register for events by going to the website (http://www.shaastra.org) and finding out the procedure to register for a specific event/workshop of interest at the event page.


Thank you,
Organizing Team,
Shaastra 2015.
                """ % (user.email, user.password, user.id)
                u = user
                print "Sending email : ", u.email
                try:
                    server.sendmail("Shaastra <shaastra@smail.iitm.ac.in>",
                        u.email, msg)
                except:
                    pass
                server.quit()
            token = Token.objects.get_or_create(user=user)[0]
            user = authenticate(username=serialized.init_data['email'][:30], password=serialized.init_data['password'])
            login(request, user)
            data = serialized.data
            data['token'] = token.key
            data['user_id'] = user.id
            return Response(data, status=status.HTTP_201_CREATED)
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny, ))
def participant_login(request):
    data = request.DATA
    email = data.get('email', None)
    password = data.get('password', None)
    if email == None:
        return Response({
            "email": ["Email or Shaastra ID is required"]
        }, status=status.HTTP_400_BAD_REQUEST)
    if password == None:
        return Response({
            "password": ["Password is required"]
        }, status=status.HTTP_400_BAD_REQUEST)

    user = get_object_or_None(User, email=email)
    if user == None:
        user = get_object_or_None(User, id=int(email.upper().replace("SH15", "")))
    if user == None:
        return Response({
            "email": ["This email address or Shaastra ID doesn't have an account."]
        }, status=status.HTTP_400_BAD_REQUEST)

    # Authenticates user against database
    user = authenticate(username=user.username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user) # Logs in the User
            profile = UserProfile.objects.get_or_create(user=user)[0]
            if profile.city and profile.mobile_number:
                valid_profile = "1"
            else:
                valid_profile = "0"

            return Response({
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'token': Token.objects.get_or_create(user=user)[0].key,
                'valid_profile': valid_profile,
                'user_id': user.id
            }, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({
                "email": ["This email is not activated."]
            }, status=status.HTTP_400_BAD_REQUEST)
    return Response({
        "email": ["The password provided does not match the email."]
    }, status=status.HTTP_400_BAD_REQUEST)

@login_required
def social_login( request ):

    user = request.user
    profile = UserProfile.objects.get_or_create(user=user)[0]
    if profile.city and profile.mobile_number:
        valid_profile = "1"
    else:
        valid_profile = "0"

    return redirect( settings.SOCIAL_AUTH_CREDENTIALS_REDIRECT +\
        '?first_name=' + user.first_name +\
        '&last_name=' + user.last_name +\
        '&email=' + user.email +\
        '&token=' + Token.objects.get_or_create(user=user)[0].key +\
        '&valid_profile=' + valid_profile +\
        '&user_id=' + format(user.id) +\
        '&redirect=true'\
    )

# --------------------------------------------------------------
# Views for Python Social auth
# Unsubscibe email
def unsubscribe(request, username, token):
    """
    User is immediately unsubscribed if they are logged in as username, or
    if they came from an unexpired unsubscribe link. Otherwise, they are
    redirected to the login page and unsubscribed as soon as they log in.
    """
    user = get_object_or_404(User, username=username, is_active=True)

    if ( (request.user.is_authenticated() and request.user == user) or user.profile.check_token(token)):
       # unsubscribe them
        profile = user.profile
        profile.send_mails = False
        profile.save()

        local_context = {}
        return render_to_response("pages/unsubscribe.html", local_context, context_instance= global_context(request))
    # Otherwise redirect to login page
    next_url = reverse('apps.users.views.unsubscribe', kwargs={'username': username, 'token': token,})
    return HttpResponseRedirect('%s?next=%s' % (reverse('login'), next_url))
