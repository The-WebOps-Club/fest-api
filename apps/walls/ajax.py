# For simple dajax(ice) functionalities
from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax

# From Django
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# For rendering templates
from django.template import RequestContext
from django.template.loader import render_to_string

# Decorators
from django.contrib.auth.decorators import login_required, user_passes_test
import json

from notifications.models import Notification
from misc.utils import *  #Import miscellaneous functions

# From Apps
from apps.walls.models import Post

# Ajax post & comment
from django.shortcuts import get_object_or_404
from apps.walls.models import Wall, Post, Comment
from annoying.functions import get_object_or_None

@dajaxice_register
def hello_world(request):
    """
        Used for testing Dajax + Dajaxice
    """
    dajax = Dajax()
    dajax.assign('body','innerHTML', "Hello world !")
    #dajax.alert("Hello World!")
    return dajax.json()
    
@dajaxice_register
def hello(request):
    """
        Used for testing Dajaxice
    """
    #html_content = render_to_string("dash/task_tables/coord_you.html", query_dictionary, RequestContext(request))
    return simplejson.dumps({'message': 'hello'})


@dajaxice_register
def newsfeed_pagination(request, page):
    items_list = Notification.objects.order_by("-timestamp")
    paginator = Paginator(items_list, 5)
    try:
        items = paginator.page(page)
        exhausted = False
    except PageNotAnInteger:
        pass
        # If page is not an integer, deliver first page.
        # items = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        items = []
        exhausted = True

    append_string = ""
    for item in items:
        append_string += render_to_string('modules/post.html', {'post': item.target}, context_instance= global_context(request))
    return json.dumps({'append_string': append_string, 'exhausted':exhausted})

@dajaxice_register
def wall_pagination(request, page, wall_id):
    posts_list = Post.objects.filter(wall__id = int(wall_id)).order_by('-time_updated')
    paginator = Paginator(posts_list, 5)
    try:
        items = paginator.page(page)
        exhausted = False
    except PageNotAnInteger:
        pass
        # If page is not an integer, deliver first page.
        # items = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        items = []
        exhausted = True

    append_string = ""
    for item in items:
        append_string += render_to_string('modules/post.html', {'post': item, 'show_post':'True'}, context_instance= global_context(request))
    return json.dumps({'append_string': append_string, 'exhausted':exhausted})

@dajaxice_register
def notifs_pagination(request, page, notif_type = 'unread'):
    if notif_type == 'unread':
        notifs_list = request.user.notifications.unread()
    elif notif_type == 'read':
        notifs_list = request.user.notifications.read()

    paginator = Paginator(notifs_list, 5)
    try:
        items = paginator.page(page)
        exhausted = False
    except PageNotAnInteger:
        pass
        # If page is not an integer, deliver first page.
        # items = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        items = []
        exhausted = True

    append_string =  render_to_string('modules/notification.html', {'notifications': items}, context_instance= global_context(request))
    return json.dumps({ 'append_string': append_string, 
    	'exhausted':exhausted, 
    	'notif_type':notif_type
    })

@dajaxice_register
def create_post(request, wall_id, new_post):
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

    # create a new post
    data = request.POST.copy()
    append_string = ""
    if new_post:
        new_post = Post.objects.create(description=new_post, wall=wall, by=request.user)
        notification_list =  data.getlist("atwho_list")
        for i in notification_list:
            i_type, i_id = i.split("_")[:-1], i.split("_")[-1]
            if i_type.lower().startswith("department"):
                i_type = "dept"
            elif i_type.lower().startswith("subdept"):
                i_type = "subdept"
                
            print new_post
        print "---------------------------------------------------"
        
        # Render the new post
        append_string =  render_to_string('modules/post.html', {'post': new_post}, context_instance= global_context(request))
    return json.dumps({ 'append_string': append_string })

@dajaxice_register
def create_comment(request, post_id, new_comment):
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
    append_string = ""
    if new_comment:
        new_comment = Comment.objects.create(description=new_comment, by=request.user)
        # Attempt to get the post for the comment
        post = get_object_or_None(Post, id=int(post_id))
        if not post:
            raise InvalidArgumentValueException("No Post with id `post_id` was found in the database")

        print "---------------------------------------------"
        print data.getlist("textarea_atwho_list")
    
        post.comments.add(new_comment)
        
        # Render the new comment
        append_string =  render_to_string('modules/comment.html', {'comment': new_comment, 'post': post}, context_instance= global_context(request))
    return json.dumps({ 'append_string': append_string })    