# Django
from django.shortcuts import get_object_or_404, render_to_response, redirect, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.dispatch import receiver
from django.db.models.signals import post_save
# Apps
from misc.utils import *  #Import miscellaneous functions
# Decorators
# Models
from django.contrib.auth.models import User
from apps.walls.models import Wall, Post, Comment
from apps.users.models import UserProfile, ERPProfile, Dept, Subdept
# View functions
# Misc
from django.templatetags.static import static
from misc import strings
from annoying.functions import get_object_or_None
# Python
import os
import notifications

def wall (request, wall_id=None):
    """
        Renders a Wall. It can be of User, Department, subdepartment etc.

        Args:
            request     :The HTTP Request:
            wall_id     :ID of the wall that has to be shown

        Kwargs:
            None

        Returns:
            If id found in database : renders 'pages/wall.html'
            > Context variables in the `pages/wall.html` :-
                - global_context_variables : misc.utils.global_context()
                - wall      :  The current wall objects
                - posts     : Posts related to the wall
        Raises:
            None
    """
    # Default argument setting and checking
    wall = None
    if wall_id == None:    
        if hasattr(request.user, "erp_profile") and hasattr(request.user.erp_profile, "wall"):
            wall_id = request.user.erp_profile.wall.id
            wall = request.user.erp_profile.wall
    else:
        # Initial validations
        try:
            wall_id = int(wall_id)
        except ValueError:
            print wall_id, "could not convert to int"
            wall_id = None
        if not ( type(wall_id) is int ):
            print "wall_id :", wall_id, type(wall_id)
            raise InvalidArgumentTypeException("`wall_id` type is wrong. Expected an integer. Got : " + str(wall_id))
        wall = get_object_or_None(Wall, id=wall_id)
    if not wall:
        raise InvalidArgumentValueException("Wall with the `wall_id` " + str(wall_id) + " not found.")
    # Logic
    wall_posts = Post.objects.filter(wall = wall).order_by('-time_updated')[:5]
    # wall_notifications = request.user.notifications.unread()
    local_context = {
    	"current_page" : "wall",
        "wall" : wall,
        "showing_user" : wall.parent.user,
        "wall_posts" : wall_posts,
    }
    if request.user.erp_profile.wall == wall:
        local_context["current_page"] = "wall"
    elif request.session["role_dept"] == wall.id:
        local_context["current_page"] = "dept_wall"
    return render_to_response('pages/wall.html', local_context, context_instance= global_context(request))

def my_wall(request, owner_type, owner_id):
    # Initial validations
    try:
        owner_id = int(owner_id)
    except ValueError:
        print owner_id, "could not convert to int"
        owner_id = None
    if not ( type(owner_type) is str or type(owner_type) is unicode ):
        print owner_id, type(owner_id)
        print owner_type, type(owner_type)
        raise InvalidArgumentTypeException
    owner_type = owner_type.lower()
    wall_id = None

    if owner_type == "user":
        wall_id = get_object_or_None(Wall, person__user__id=owner_id if owner_id else request.user.id)
        if wall_id:
            wall_id = wall_id.id
    elif owner_type == "subdept":
        if owner_id:
            wall_id = get_object_or_None(Wall, subdept__id=owner_id)
            if wall_id:
            	wall_id = wall_id.id
        else:
            if request.session["role"] == "coord":
                wall_id = get_object_or_None(Wall, subdept__id=request.session["role_dept"])
                if wall_id:
            		wall_id = wall_id.id
    elif owner_type == "dept":
        if owner_id:
            wall_id = get_object_or_None(Wall, dept__id=owner_id)
            if wall_id:
            	wall_id = wall_id.id
        else:
            if request.session["role"] == "coord":
                dept_id = get_object_or_None(Subdept, id=request.session["role_dept"])
                if dept_id:
                    dept_id = dept_id.dept.id
                    wall_id = get_object_or_None(Wall, dept__id=dept_id)
                    if wall_id:
            			wall_id = wall_id.id
            else: # supercoord and core
                wall_id = get_object_or_None(Wall, dept__id=request.session["role_dept"])
                if wall_id:
            		wall_id = wall_id.id

    if wall_id == None:
        raise InvalidArgumentValueException
    return redirect(reverse("wall", kwargs={"wall_id" : wall_id}))
