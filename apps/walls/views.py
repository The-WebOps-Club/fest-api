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
from models import Wall, Post
# Forms
# View functions
# Misc
from django.templatetags.static import static
from misc import strings
# Python
import os


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
    wallpage = True
    if wall_id:
        wall = get_object_or_404(Wall, pk=int(wall_id))
    else:
        wall = request.user.erp_profile.wall
    posts = Post.objects.filter(wall=wall).order_by('-time_updated')
    return render_to_response('pages/wall.html', locals(), context_instance= global_context(request))

def create_post(request, wall_id):
    """
        Create a new wall post
    """
    wallpage = True
    data = request.POST.copy()
    try:
        wall = get_object_or_404(Wall, pk=int(wall_id))
        Post.objects.create(description=data['status'], 
            wall=wall, by=request.user)
    except Exception, e:
        messages.error(request, strings.STD_ERROR %(str(e.message)))
    return redirect('wall', wall_id=wall.pk) # Newsfeeed? Need to provode a proper redirect method

def create_comment(request, post_id):
    """
        Creates a new comment on a Post
    """
    wallpage = True
    data = request.POST.copy()
    # try:
    parent_post = get_object_or_404(Post, pk=post_id)
    new_comment = Post.objects.create(description=data['status'], 
            by=request.user)
    parent_post.childs.add(new_comment)
    # parent_post.save()
    # except Exception, e:
    messages.error(request, strings.STD_ERROR )
    return redirect('wall', wall_id=parent_post.wall.pk)


