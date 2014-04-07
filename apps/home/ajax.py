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
    return json.dumps({'message': 'hello'})

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
    return json.dumps({'append_string': append_string, 'exhausted':exhausted, 'notif_type':notif_type})