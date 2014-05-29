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
from apps.walls.utils import get_my_posts
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
    user = request.user
    if hasattr(user, "erp_profile"):
        user_erp_profile = user.erp_profile
    else:
        user_erp_profile = None
    wall = None
    if wall_id == None:    
        if user_erp_profile and hasattr(request.user.erp_profile, "wall"):
            wall = user_erp_profile.wall
            wall_id = wall.id
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

    wall_accessible = True

    # Logic
        # Check wall conditions
    if not wall:
        raise InvalidArgumentValueException("Wall with the `wall_id` " + str(wall_id) + " not found.")
    elif not wall.has_access(user) and not user.is_superuser:
        wall_accessible = False
    
        # Get wall posts
    if not wall_accessible:
        wall_posts = get_my_posts(user, wall)[:5]
    if wall_accessible:
        wall_posts = Post.objects.filter(wall=wall).order_by('-time_created')[:5]
    
    wall_parent = wall.parent

    local_context = {
        "current_page" : "wall",
        "wall" : wall,
        "showing_user" : wall_parent,
        "wall_posts" : wall_posts,
        "wall_accessible" : wall_accessible,
    }
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
        raise InvalidArgumentTypeException("owner_id : " + str(owner_id) + " is of type " + type(owner_id) + " ... owner_type" + str(owner_type) + " is of type " + type(owner_type))
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
    elif owner_type == "page":
        if owner_id:
            wall_id = get_object_or_None(Wall, page__id=owner_id)
            if wall_id:
                wall_id = wall_id.id
        else:
            raise InvalidArgumentValueException("Got no `owner_id` for `owner_type` = " + owner_type)
    if wall_id == None:
        raise InvalidArgumentValueException("Got no wall for `owner_id` = " + owner_id + " and `owner_type` = " + owner_type)
    return redirect(reverse("wall", kwargs={"wall_id" : wall_id}))
