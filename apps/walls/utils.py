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

def filetag_to_url(tag):
    # --@@!@@-- acts as a common delimiter.
    filename, fileid, iconlink = tag.split('--@@!@@--');
    return reverse("view")+'?id='+fileid, filename, iconlink; 

# TODO: merge parse_atwho ad parse_atwho_file
def parse_atwho_file( my_text, tags ):
    """
        Parses through the list form atwho and records file references.
    """
    notification_list = []
    link_text = '![Doc](%s) [%s](%s)'
    for tag in tags:
            url, filename, iconLink = filetag_to_url( tag )
            my_text = my_text.replace(':' + filename, (link_text %(iconLink, filename, url) ))
    return my_text

def parse_atwho(my_text, tags, at='@' ):
    """
        Parses through the list form atwho and gives the depts, subdepts and users
    """
    notification_list = []
    link_text = '![%s](%s) [%s](%s)' # alt_text, icon_link, name, wall_link
    for tag in tags:
        tagged_obj = get_tag_object(tag)
        if isinstance(tagged_obj, Dept):
            alt_text = "Dept"
            icon_link = "/static/img/dept.png"
        elif isinstance(tagged_obj, Subdept):
            alt_text = "Subdept"
            icon_link = "/static/img/subdept.png"
        if isinstance(tagged_obj, Dept):
            alt_text = "Dept"
            icon_link = "/static/img/dept.png"
        else:
            alt_text = "User"
            icon_link = "/static/img/user.png"

        if isinstance(tagged_obj, Dept) or isinstance(tagged_obj, Subdept):
            link_href = reverse("wall", kwargs={"wall_id" : tagged_obj.wall.pk})
            my_text = my_text.replace(at + tagged_obj.name, link_text % (alt_text, icon_link, tagged_obj.name, link_href) )
        else:
            link_href = reverse("wall", kwargs={"wall_id" : tagged_obj.erp_profile.wall.pk})
            my_text = my_text.replace(at + tagged_obj.first_name+"_"+tagged_obj.last_name, link_text %(alt_text, icon_link, tagged_obj.get_full_name(), link_href) )
        notification_list.append(tagged_obj)
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
