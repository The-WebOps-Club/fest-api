# For simple dajax(ice) functionalities
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
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
from apps.users.models import UserProfile, ERPProfile, Dept, Subdept
from apps.walls.utils import paginate_items

# Ajax post & comment
from django.shortcuts import get_object_or_404
from apps.walls.models import Wall, Post, Comment
from annoying.functions import get_object_or_None

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
# PAGINATIONS AND INFINITE SCROLLS
@dajaxice_register
def newsfeed_pagination(request, page, **kwargs):
    notifications_list = Notification.objects.order_by("-timestamp")
    items, exhausted = paginate_items(notifications_list, page=page, **kwargs)
    append_string = ""
    for item in items:
        local_context = {
            'post' : item.target, 
            'notification' : item,
        }
        append_string += "<hr />" \
            + render_to_string('modules/post.html', local_context, context_instance= global_context(request))
    local_context = {
        "append_string" : append_string,
        "exhausted" : exhausted,
    }
    return json.dumps(local_context)

@dajaxice_register
def wall_pagination(request, page, wall_id, **kwargs):
    posts_list = Post.objects.filter(wall__id = int(wall_id)).order_by('-time_updated')
    items, exhausted = paginate_items(posts_list, page=page, **kwargs)
    append_string = ""
    for item in items:
        local_context = {
            'post' : item, 
            'show_post' : 'True',
        }
        append_string += "<hr />" \
            + render_to_string('modules/post.html', local_context, context_instance= global_context(request))
    local_context = {
        "append_string" : append_string,
        "exhausted" : exhausted,
        "wall_id" : wall_id,
    }
    return json.dumps(local_context)

@dajaxice_register
def notifs_pagination(request, page, notif_type='unread', **kwargs):
    if notif_type == 'unread':
        notifs_list = request.user.notifications.unread()
    elif notif_type == 'read':
        notifs_list = request.user.notifications.read()
    elif notif_type == 'all':
        notifs_list = request.user.notifications.all()
    items, exhausted = paginate_items(notifs_list, page=page, **kwargs)
    append_string = ""
    for item in items:
        local_context = {
            'notification' : item,
        }
        append_string += render_to_string('modules/notif.html', local_context, context_instance= global_context(request))
    local_context = {
        "append_string" : append_string,
        "exhausted" : exhausted,
    }
    return json.dumps(local_context)

@dajaxice_register
def comments_pagination(request, page, post_id, **kwargs):
    comments_list = Post.objects.filter(post__id = int(post_id)).order_by('-time_created')
    items, exhausted = paginate_items(comments_list, page=page, **kwargs)
    append_string = ""
    for item in items:
        local_context = {
            'notification' : item,
        }
        append_string += render_to_string('modules/notif.html', local_context, context_instance= global_context(request))
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
    print wall

    # create a new post
    data = request.POST.copy()
    append_string = ""
    if post_form:
        data = deserialize_form(post_form)
        post_text = data['new_post']
        tags =  data.getlist("atwho_list")
        parsed_tags = [tag.rsplit("_",1) for tag in tags]
        notification_depts = []
        notification_subdepts = []
        notification_users = []
        link_text = '<a href="%s"> %s</a>'
        for tag in parsed_tags:
            id = int(tag[1])
            key = tag[0]
            if key == 'department':
                tagged_dept = get_object_or_None(Dept, id=id)
                if tagged_dept:
                    notification_depts.append(tagged_dept)
                    post_text = post_text.replace('@' + tagged_dept.name, link_text %(reverse("wall", kwargs={"wall_id" : tagged_dept.wall.pk}), tagged_dept.name) )
                else:
                    print "No id for dept"
            elif key == 'subdept':
                tagged_subdept = get_object_or_None(Subdept, id=id)
                if tagged_subdept:
                    notification_subdepts.append(tagged_subdept)
                    post_text = post_text.replace('@' + tagged_subdept.name, link_text %(reverse("wall", kwargs={"wall_id" : tagged_subdept.wall.pk}), tagged_subdept.name) )
                else:
                    print "No id for subdept"
            else:
                tagged_user = get_object_or_None(User, id=id)
                if tagged_user:
                    notification_users.append(tagged_user)
                    post_text = post_text.replace('@' + tagged_user.first_name+"_"+tagged_user.last_name, link_text %(reverse("wall", kwargs={"wall_id" : tagged_user.erp_profile.wall.pk}), tagged_user.get_full_name()) )
                else:
                    print "No id for user"

        new_post = Post.objects.create(description=post_text, wall=wall, by=request.user)

        if notification_depts:
            new_post.notification_depts.add(tagged_dept)
        if notification_subdepts:
            new_post.notification_subdepts.add(tagged_subdept)
        if notification_users:
            new_post.notification_users.add(tagged_user)
        # Render the new post
        append_string =  render_to_string('modules/post.html', {'post': new_post}, context_instance= global_context(request)) + "<hr />"
    return json.dumps({ 'append_string': append_string })

@dajaxice_register
def create_comment(request, post_id, comment_form):
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
    if comment_form:
        data = deserialize_form(comment_form)
        print data
        # Attempt to get the post for the comment
        post = get_object_or_None(Post, id=int(post_id))
        comment_text = data['comment']
        if not post:
            raise InvalidArgumentValueException("No Post with id `post_id` was found in the database")

        print "---------------------------------------------"
        tags = data.getlist("atwho_list")
        # Gives the first and last words after splitting with underscore.
        # First id and last is keyword (department, subdepartment and any others: email)
        parsed_tags = [tag.rsplit("_",1) for tag in tags]
        notification_depts = []
        notification_subdepts = []
        notification_users = []
        link_text = '<a href="%s"> %s</a>'
        for tag in parsed_tags:
            id = int(tag[1])
            key = tag[0]
            if key == 'department':
                tagged_dept = get_object_or_None(Dept, id=id)
                if tagged_dept:
                    notification_depts.append(tagged_dept)
                    comment_text = comment_text.replace('@' + tagged_dept.name, link_text %(reverse("wall", kwargs={"wall_id" : tagged_dept.wall.pk}), tagged_dept.name) )
                else:
                    print "No id for dept"
            elif key == 'subdept':
                tagged_subdept = get_object_or_None(Subdept, id=id)
                if tagged_subdept:
                    notification_subdepts.append(tagged_subdept)
                    comment_text = comment_text.replace('@' + tagged_subdept.name, link_text %(reverse("wall", kwargs={"wall_id" : tagged_subdept.wall.pk}), tagged_subdept.name) )
                else:
                    print "No id for subdept"
            else:
                tagged_user = get_object_or_None(User, id=id)
                if tagged_user:
                    notification_users.append(tagged_user)
                    comment_text = comment_text.replace('@' + tagged_user.first_name+"_"+tagged_user.last_name, link_text %(reverse("wall", kwargs={"wall_id" : tagged_user.erp_profile.wall.pk}), tagged_user.get_full_name()) )
                else:
                    print "No id for user"

        new_comment = Comment.objects.create(description=comment_text, by=request.user)
        post.comments.add(new_comment)
        if notification_depts:
            post.notification_depts.add(tagged_dept)
        if notification_subdepts:
            post.notification_subdepts.add(tagged_subdept)
        if notification_users:
            post.notification_users.add(tagged_user)
        # Render the new comment
        append_string =  render_to_string('modules/comment.html', {'comment': new_comment, 'post': post}, context_instance= global_context(request))
    return json.dumps({ 'append_string': append_string })    