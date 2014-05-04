# From Django
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext
from django.template.loader import render_to_string
from django.templatetags.static import static
from django.shortcuts import get_object_or_404
# Decorators
from django.contrib.auth.decorators import login_required, user_passes_test
# Python
from misc.utils import *  #Import miscellaneous functions
# From Apps
from apps.users.models import UserProfile, ERPProfile, Dept, Subdept
from notifications.models import Notification
# Ajax post & comment
from apps.walls.models import Wall, Post, Comment
from annoying.functions import get_object_or_None
import json
import re

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

def filetag_to_url(tag):
    # --@@!@@-- acts as a common delimiter.
    filename, fileid, iconlink = tag.split('--@@!@@--');
    return reverse("view")+'?id='+fileid, filename, iconlink; 

# TODO: merge parse_atwho and parse_atwho_file
def parse_atwho(my_text):
    """
        Parses through the list form atwho and records file, dept, subdept, user references.
    """
    notification_list = []
    
    link_regex = re.compile("\[(.*?)\] \((.*?)\)", re.IGNORECASE)
    link_list = link_regex.findall(my_text)
    for i in link_list:
        filename, iconLink, data = docs_list
        _type, _id = data.split("#", 1)
        # if _type == "doc":
        #     pass
        #     _url = reverse("view") + "?id=" + _id
        # else:
        #     _url = reverse("my_wall", kwargs={"owner_type":_type, "owner_id":_id})
        if _type == "user":
            notification_list.append(User.objects.get(id=_id))
        elif _type == "subdept":
            notification_list.append(Subdept.objects.get(id=_id))
        elif _type == "dept":
            notification_list.append(Dept.objects.get(id=_id))

    return my_text, notification_list
    
def get_tag_object(tag):
    # `tags` Gives the first and last words after splitting with underscore.
    # First id and last is keyword (department, subdepartment and any others: email)
    if not isinstance(tag, list) and ( isinstance(tag, basestring) ):
        tag = tag.rsplit("_", 1)
    print tag
    print "---------------------------"
    tag_id = int(tag[1])
    key = tag[0].lower()
    if key == "department":
        obj = get_object_or_None(Dept, id=tag_id)
    elif key == "subdept":
        obj = get_object_or_None(Subdept, id=tag_id)
    else:
        obj = get_object_or_None(User, id=tag_id)
    return obj

def notification_query():
    post_set = set()
    post_set.update(Notification.objects.values_list("target_object_id", flat=True))
    

    return Notification.objects.order_by("-timestamp")
