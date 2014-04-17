# From Django
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext
from django.template.loader import render_to_string
# Decorators
from django.contrib.auth.decorators import login_required, user_passes_test
# Python
from misc.utils import *  #Import miscellaneous functions
# From Apps
from apps.users.models import UserProfile, ERPProfile, Dept, Subdept
from notifications.models import Notification
# Ajax post & comment
from django.shortcuts import get_object_or_404
from apps.walls.models import Wall, Post, Comment
from annoying.functions import get_object_or_None
import json
    
def paginate_items(items_list, **kwargs):
    """
        Possible kwargs :
            page : int - The page you wish to see
            max_items : int - The max number of items in a page

    """
    max_items = kwargs.get("max_items", 5)
    page = kwargs.get("page", 1)
    paginator = Paginator(items_list, max_items)
    exhausted = False
    items = []
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        pass
    except EmptyPage:
        exhausted = True
    return items, exhausted

def create_posts_page(request, items_list, **kwargs):
    items, exhausted = paginate_items(items_list, **kwargs)
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
    }
    return local_context

def create_notifications_page(request, items_list, **kwargs):
    items, exhausted = paginate_items(items_list, **kwargs)
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
    return local_context

def create_notifs_page(request, items_list, **kwargs):
    items, exhausted = paginate_items(items_list, **kwargs)
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
    return local_context