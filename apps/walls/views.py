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
# Forms

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
	wall_posts = Post.objects.filter(wall = wall).order_by('-time_updated')[:5]
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
	if not ( type(owner_type) is str or type(owner_type) is unicode ):
		print owner_id, type(owner_id)
		print owner_type, type(owner_type)
		raise InvalidArgumentTypeException
	owner_type = owner_type.lower()
	wall = None

	if owner_type == "user":
		wall = get_object_or_404(Wall, person__user__id=owner_id if owner_id else request.user.id)
		
	elif owner_type == "subdept":
		if owner_id:
			wall = get_object_or_404(Wall, subdept__id=owner_id)
		else:
			if request.session["role"] == "coord":
				wall = get_object_or_404(Wall, subdept__id=request.session["role_dept"])
	elif owner_type == "dept":
		if owner_id:
			wall = get_object_or_404(Wall, dept__id=owner_id)
		else:
			if request.session["role"] == "coord":
				dept_id = get_object_or_404(Subdept, id=request.session["role_dept"])
				if dept_id:
					dept_id = dept_id.dept.id
					wall = get_object_or_404(Wall, dept__id=dept_id)
			else: # supercoord and core
				wall = get_object_or_404(Wall, dept__id=request.session["role_dept"])

	if wall == None:
		raise InvalidArgumentValueException
	return redirect(reverse("wall", kwargs={"wall_id" : wall.id}))


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
		raise InvalidArgumentTypeException("argument `wall_id` should be of type integer")
	wall = get_object_or_404(Wall, id=int(wall_id))
	print wall
	data = request.POST.copy()
	if data.get("new_post", None):
		new_post = Post.objects.create(description=data['new_post'], wall=wall, by=request.user)
		notification_list =  data.getlist("atwho_list")
		for i in notification_list:
			i_type, i_id = i.split("_")[:-1], i.split("_")[-1]
			if i_type.lower().startswith("department"):
				i_type = "dept"
			elif i_type.lower().startswith("subdept"):
				i_type = "subdept"
				
			print new_post
		print "---------------------------------------------------"
		return redirect('wall', wall_id=wall.pk)
	else:
		return redirect(request.META.get('HTTP_REFERER', '/'))
	
	

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
		raise InvalidArgumentTypeException("argument `post_id` should be of type integer")
	
	# Create a new comment
	data = request.POST.copy()
	if data.get("comment", None):
		new_comment = Comment.objects.create(description=data['comment'], by=request.user)
		# Attempt to get the post for the comment
		post = get_object_or_None(Post, id=int(post_id))
		if not post:
			raise InvalidArgumentValueException("No Post with id `post_id` was found in the database")

		print "---------------------------------------------"
		print data.getlist("textarea_atwho_list")
	
		post.comments.add(new_comment)
		return redirect('wall', wall_id=post.wall.pk)
	else:
		return redirect(request.META.get('HTTP_REFERER', '/'))

# def add_notification_users(__name__list, ):
