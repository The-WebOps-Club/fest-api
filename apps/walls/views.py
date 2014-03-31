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
from models import Wall, Post, Comment
# Forms
# View functions
# Misc
from django.templatetags.static import static
from misc import strings
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
            raise InvalidArgumentTypeException
        wall = get_object_or_404(Wall, id=wall_id)

    # Logic
    wall_posts = Post.objects.filter(wall = wall).order_by('-time_updated')
    # wall_notifications = request.user.notifications.unread()

    local_context = {
        "wall" : wall,
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
	if not ( type(owner_type) is str or type(owner_type) is unicode ) or type(owner_id) is not int:
		print owner_id, type(owner_id)
		print owner_type, type(owner_type)
		raise InvalidArgumentTypeException
	
	wall_id = None
	if owner_type == "user":
		wall_id = request.user.erp_profile.wall.id
	else:
		if request.session["role"] == "coord":
			if owner_type == "subdept":
				wall_id = Subdept.objects.get(id = request.session["role_dept"]).wall.id
			elif owner_type == "dept":
				wall_id = Subdept.objects.get(id = request.session["role_dept"]).dept.wall.id
		elif owner_type == "core" or owner_type == "supercoord":
			if owner_type == "dept":
				wall_id = Dept.objects.get(id = request.session["role_dept"]).wall.id
	if wall_id == None:
		raise InvalidArgumentValueException
	return redirect(reverse("wall", kwargs={"wall_id" : wall_id}))


def create_post(request, wall_id):
    """
        Create a new wall post
    """
    # Initial validations
    try:
        wall_id = int(wall_id)
    except ValueError:
        print wall_id, "could not convert to int"
        wall_id = None
    if not ( type(wall_id) is int ):
        print "wall_id :", wall_id, type(wall_id)
        raise InvalidArgumentTypeException
    wall = get_object_or_404(Wall, id=int(wall_id))
    
    data = request.POST.copy()
    if not request.user in wall.owners.all():
        messages.error(request, strings.STD_ERROR %('You dont have permission to post here'))
        return redirect('wall', wall_id=wall.pk)
    Post.objects.create(description=data['new_post'], wall=wall, by=request.user)
    
    return redirect('wall', wall_id=wall.pk)

def create_comment(request, post_id):
    """
        Creates a new comment on a Post
    """
    # Initial validations
    try:
        post_id = int(post_id)
    except ValueError:
        print post_id, "could not convert to int"
        post_id = None
    if not ( type(post_id) is int ):
        print "post_id :", post_id, type(post_id)
        raise InvalidArgumentTypeException
    post = get_object_or_404(Post, id=int(post_id))

    data = request.POST.copy()
    new_comment = Comment.objects.create(description=data['comment'], by=request.user)
    post.comments.add(new_comment)
    #post.comments_count += 1
    #post.save()
    
    return redirect('wall', wall_id=post.wall.pk)


# Gen testing views
def show_wall (request, wall_id=None):
    return render_to_response('pages/wall.html', locals(), context_instance= global_context(request))
