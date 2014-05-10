# For simple dajax(ice) functionalities
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from dajax.core import Dajax

# From Django
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# For rendering templates
from django.template import RequestContext, Template
from django.template.loader import render_to_string

# Decorators
from django.contrib.auth.decorators import login_required, user_passes_test
import json

from notifications.models import Notification
from misc.utils import *  #Import miscellaneous functions

# From Apps
from apps.users.models import UserProfile, ERPProfile, Dept, Subdept
from apps.walls.utils import paginate_items, parse_atwho, get_tag_object

# Ajax post & comment
from django.shortcuts import get_object_or_404
from apps.walls.models import Wall, Post, Comment
from annoying.functions import get_object_or_None
# Parse HTML: prevention of deliberate code injection.


# -------------------------------------------------------------
# TEST FUNCTIONS
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

# -------------------------------------------------------------
# GENERAL AJAXED FUNCTIONS
@dajaxice_register
def mark_as_read(request, **kwargs):
    all_notifs = user.notifications.unread()
    for i in all_notifs:
        i.public = False
        i.save()
    all_notifs.mark_all_as_read()
    return json.dumps({"msg" : "done"})

@dajaxice_register
def like_post(request, id=None):
    if not id:
        return json.dumps({"msg" : "error"})
    Post.objects.get(id=id).liked_users.add(request.user)
    return json.dumps({"msg" : "done"})

@dajaxice_register
def like_comment(request, id=None):
    if not id:
        return json.dumps({"msg" : "error"})
    Comment.objects.get(id=id).liked_users.add(request.user)
    return json.dumps({"msg" : "done"})

# -------------------------------------------------------------
# PAGINATIONS AND INFINITE SCROLLS
@dajaxice_register
def get_notifications(request, **kwargs):
    page = kwargs.get("page", None)
    notification_id = kwargs.get("id", None)
    exhausted = False
    max_items = kwargs.get("max_items", 5)
    notifications_list = Notification.objects.all()
    if page:    
        items = Notification.objects.raw("""
            SELECT a.* 
            FROM notifications_notification a 
            WHERE NOT EXISTS (
                SELECT 1 
                FROM notifications_notification 
                WHERE target_object_id = a.target_object_id 
                    AND timestamp > a.timestamp
            ) 
            GROUP BY a.target_object_id
            ORDER BY a.timestamp DESC
            LIMIT """ + str((page-1)*max_items) + "," + str(page*max_items))
    elif notification_id:
        items = notification_lists.filter(id=notification_id)

    append_string = ""
    for item in items:
        local_context = {
            'post' : item.target, 
            'notification' : item,
        }
        append_string += render_to_string('modules/post.html', local_context, context_instance=global_context(request, token_info=False))
    local_context = {
        "append_string" : append_string,
        "exhausted" : exhausted,
    }
    return json.dumps(local_context)

@dajaxice_register
def get_posts(request, **kwargs):
    page = kwargs.get("page", None)
    wall_id = kwargs.get("wall_id", None)
    post_id = kwargs.get("id", None)
    exhausted = False
    if wall_id:
        posts_list = Post.objects.filter(wall__id = int(wall_id)).order_by('-time_updated')
    else:
        posts_list = Post.objects.all().order_by('-time_updated')

    if page:
        items, exhausted = paginate_items(posts_list, **kwargs)
    elif post_id:
        items = posts_list.filter(id = int(post_id))
    
    append_string = ""
    for item in items:
        local_context = {
            'post' : item, 
            'show_post' : 'True',
        }
        append_string += "<hr />" \
            + render_to_string('modules/post.html', local_context, context_instance= global_context(request, token_info=False))
    local_context = {
        "append_string" : append_string,
        "exhausted" : exhausted,
        "wall_id" : wall_id,
    }
    return json.dumps(local_context)

@dajaxice_register
def get_notifs(request, **kwargs):
    page = kwargs.get("page", None)
    notif_type = kwargs.get("notif_type", None)
    notif_id = kwargs.get("id", None)
    exhausted = False
    if notif_type == 'unread':
        notifs_list = request.user.notifications.unread()
    elif notif_type == 'read':
        notifs_list = request.user.notifications.read()
    else:    
        notifs_list = request.user.notifications.all()

    if page:
        items, exhausted = paginate_items(notifs_list, **kwargs)
    elif notif_id:
        items = notif_list.filter(id=notif_id)

    append_string = ""
    for item in items:
        local_context = {
            'notification' : item,
        }
        append_string += render_to_string('modules/notif.html', local_context, context_instance=global_context(request, token_info=False))
    local_context = {
        "append_string" : append_string,
        "exhausted" : exhausted,
    }
    return json.dumps(local_context)

@dajaxice_register
def get_comments(request, **kwargs):
    page = kwargs.get("page", None)
    post_id = kwargs.get("post_id", None)
    comment_id = kwargs.get("id", None)
    exhausted = False
    
    if post_id:
        comments_list = Post.objects.get(id = int(post_id)).comments.order_by('-time_created')
    else:
        comments_list = Comment.objects.all()
    
    if page:
        items, exhausted = paginate_items(comments_list, **kwargs)
    elif comment_id:
        items = comments_list.filter(id=comment_id)

    append_string = ""
    items = [i for i in items][::-1]
    for item in items:
        local_context = {
            'comment' : item,
        }
        append_string += render_to_string('modules/comment.html', local_context, context_instance=global_context(request, token_info=False))
    local_context = {
        "append_string" : append_string,
        "exhausted" : exhausted,
        "post_id" : post_id,
    }
    return json.dumps(local_context)

# -------------------------------------------------------------
# CREATE STUFF
@dajaxice_register
def create_post(request, wall_id, post_form):
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

    # create a new post
    append_string = ""
    data = deserialize_form(post_form)
   
    post_text = data["new_post"]
    post_subject = data["new_post_subject"]
    print post_subject, "<<<----------------------------------------"
    post_text, notification_list = parse_atwho(post_text)

    new_post = Post.objects.create(subject=post_subject, description=post_text, wall=wall, by=request.user)

    new_post.add_notifications(notification_list)
    if wall.parent:
        new_post.add_notifications([wall.parent, request.user]) # add to and from

    new_post.send_notif()
    
    # Render the new post
    append_string =  render_to_string('modules/post.html', {'post': new_post}, context_instance=global_context(request, token_info=False)) + "<hr />"
    
    return json.dumps({ 'append_string': append_string })

@dajaxice_register
def quick_post(request, post_form):
    """
        Create a new wall post
    """
    # create a new post
    append_string = ""
    data = deserialize_form(post_form)
    print data
    post_text = data["quick_post"]
    post_text, notification_list = parse_atwho(post_text)

    # Figure out where to create post !
    to_list = data.getlist("quick_post_to")
    for i in to_list:
        print i
        print "---------------------------"
        obj = get_tag_object(i)
        if isinstance(obj, Dept) or isinstance(obj, Subdept):
            obj_wall =  obj.wall
        else:
            obj_wall =  obj.erp_profile.wall
        new_post = Post.objects.create(description=post_text, wall=obj_wall, by=request.user)
        new_post.add_notifications(notification_list)
        if obj_wall.parent:
            new_post.add_notifications([obj_wall.parent, request.user]) # add to and from

        new_post.send_notif()
    # Render the new post
    append_string =  render_to_string('modules/post.html', {'post': new_post}, context_instance=global_context(request, token_info=False)) + "<hr />"
    return json.dumps({ 'append_string': append_string })

@dajaxice_register
def create_comment(request, post_id, csrf_data, comment):
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
    append_string = ""
    data = deserialize_form(csrf_data).dict()
    
    data['comment'] = comment
    print data
    # Attempt to get the post for the comment
    post = get_object_or_None(Post, id=int(post_id))
    comment_text = data['comment']
    if not post:
        raise InvalidArgumentValueException("No Post with id `post_id` was found in the database")

    comment_text, notification_list = parse_atwho(comment_text)

    rendered_comment = Template('{%load markdown_tags%}{{comment_text|markdown}}').render(RequestContext(request,{'comment_text':comment_text}))

    new_comment = Comment.objects.create(description=rendered_comment, by=request.user)
    post.comments.add(new_comment)
    
    post.add_notifications(notification_list)
    post_wall = post.wall
    if post_wall.parent:
        post.add_notifications([post_wall.parent, request.user]) # add to and from

    new_comment.send_notif() # Send notifs now, as all notif personnel are added
    
    # Render the new comment
    local_context = {
        'comment': new_comment, 
        'post': post
    }
    append_string =  render_to_string( 'modules/comment.html', local_context, context_instance=global_context(request, token_info=False))

    local_context = { 
        'append_string': append_string,
        'post_id' : post_id
    }
    return json.dumps(local_context)
