# For simple dajax(ice) functionalities
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form

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
from apps.walls.utils import paginate_items, parse_atwho, get_tag_object, query_newsfeed, query_notifs, get_my_posts, check_access_rights, check_admin_access_rights

# Ajax post & comment
from django.shortcuts import get_object_or_404
from apps.walls.models import Wall, Post, Comment
from annoying.functions import get_object_or_None
# Parse HTML: prevention of deliberate code injection.


# -------------------------------------------------------------
# TEST FUNCTIONS    
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
def read_notif(request, notif_id, wall_id=None):
    user = request.user
    if notif_id == "all":
        notifs_list = user.notifications.unread()
    elif wall_id:
        notifs_list = user.notifications.unread().filter( description__contains = 'wall:'+wall_id )
    else:
        try:
            notif_id = int(notif_id)
        except ValueError:
            return json.dumps( { 'error' : 'notif_id was not an integer' } )
        notifs_list = user.notifications.filter(id = notif_id)
        if notifs_list.count() == 0:
            return json.dumps( { 'error' : 'no notif with the given notif_id was found' } )

    for i in notifs_list:
        i.public = False
        i.save()
    notifs_list.mark_all_as_read()
    return json.dumps( { 'success' : 'Successfully marked as read' } )
    
"""
Dosent make sense.
@dajaxice_register
def make_page_public( request, page_id ):

    wall = Wall.objects.get( page__id = page_id )
    if not ((request.user.is_superuser) or  request.user.is_staff):
        return json.dumps({"msg":"No Access Rights"})

    wall.is_public = True;
    wall.save();
    return json.dumps({"msg" : "done"})

@dajaxice_register
def make_page_private( request, page_id ):
    wall = Wall.objects.get( page__id = page_id )
    if not ((request.user.is_superuser) or request.user.is_staff):
        return json.dumps({"msg":"No Access Rights"})

    wall.is_public = False;
    wall.save();
    return json.dumps({"msg" : "done"})

"""

@dajaxice_register
def make_post_public( request, post_id ):

    post = Post.objects.get(id=post_id)
    if not (check_admin_access_rights( request.user, post )):
        return json.dumps({"msg":"No Access Rights"})

    post.is_public = True;
    post.save();
    return json.dumps({"msg" : "done"})

@dajaxice_register
def make_post_private( request, post_id ):
    post = Post.objects.get(id=post_id)
    if not (check_admin_access_rights( request.user, post )):
        return json.dumps({"msg":"No Access Rights"})

    post.is_public = False;
    post.save();
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
    user = request.user

    if page:
        items = query_newsfeed(request.user, **kwargs)
    elif notification_id:
        items = Notification.objects.filter(id=notification_id, recipient_id=user.id)
    else:
        items = Notification.objects.filter(recipient_id=user.id)

    append_string = ""
    for item in items:
        local_context = {
            'post' : item.target, 
            'notification' : item,
        }
        append_string += render_to_string('modules/post.html', local_context, context_instance=global_context(request, token_info=False))
    if append_string == "":
        exhausted = True
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
    user = request.user

    if wall_id:
        posts_list = get_my_posts(user, Wall.objects.filter(id = wall_id)[0]).order_by('-time_created');
    else:
        posts_list = get_my_posts(user).order_by('-time_created')

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
    user = request.user

    if notif_id:
        items = user.notifications.filter(id=notif_id)
    else:
        items = query_notifs(user, **kwargs)
    
    append_string = ""
    for item in items:
        local_context = {
            'notification' : item,
        }
        append_string += render_to_string('modules/notif.html', local_context, context_instance=global_context(request, token_info=False))
    if append_string == "":
        exhausted = True
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
        wall_id = None
    
    if not ( type(wall_id) is int ):
        raise InvalidArgumentTypeException("argument `wall_id` should be of type integer")
    wall = get_object_or_404(Wall, id=int(wall_id))

    # create a new post
    append_string = ""
    data = deserialize_form(post_form)
   
    post_text = data["new_post"]
    post_subject = data["new_post_subject"]
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
    post_text = data["quick_post"]
    post_text, notification_list = parse_atwho(post_text)

    # Figure out where to create post !
    to_list = data.getlist("quick_post_to")
    for i in to_list:
        obj = get_tag_object(i)
        if isinstance(obj, Dept) or isinstance(obj, Subdept) or isinstance(obj, Post):
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
def create_comment(request, post_id, data):
    """
        Creates a new comment on a Post
    """
    # Initial validations
    try:
        post_id = int(post_id)
    except ValueError:
        post_id = None
    if not ( type(post_id) is int ):
        raise InvalidArgumentTypeException("argument `post_id` should be of type integer")
    
    # Create a new comment
    append_string = ""
    data = deserialize_form(data).dict()

    
    # Attempt to get the post for the comment
    post = get_object_or_None(Post, id=int(post_id))
    comment_text = data['comment']
    if not post:
        raise InvalidArgumentValueException("No Post with id `post_id` was found in the database")

    comment_text, notification_list = parse_atwho(comment_text)

    rendered_comment = Template('{%load markdown_tags%}{%autoescape off%}{{comment_text|markdown}}{%endautoescape%}').render(RequestContext(request,{'comment_text':comment_text}))

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
