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

def parse_atwho(my_text, tags):
    """
        Parses through the list form atwho and gives the depts, subdepts and users
    """
    # `tags` Gives the first and last words after splitting with underscore.
    # First id and last is keyword (department, subdepartment and any others: email)
    
    parsed_tags = [tag.rsplit("_",1) for tag in tags]
    notification_list = []
    link_text = '[%s](%s)'
    for tag in parsed_tags:
        tag_id = int(tag[1])
        key = tag[0]
        if key == 'department':
            tagged_dept = get_object_or_None(Dept, id=tag_id)
            if tagged_dept:
                notification_list.append(tagged_dept)
                link_href = reverse("wall", kwargs={"wall_id" : tagged_dept.wall.pk})
                my_text = my_text.replace('@' + tagged_dept.name, link_text % (tagged_dept.name, link_href) )
            else:
                print "No id for dept"
        elif key == 'subdept':
            tagged_subdept = get_object_or_None(Subdept, id=tag_id)
            if tagged_subdept:
                notification_list.append(tagged_subdept)
                link_href = reverse("wall", kwargs={"wall_id" : tagged_subdept.wall.pk})
                my_text = my_text.replace('@' + tagged_subdept.name, link_text %(tagged_subdept.name, link_href) )
            else:
                print "No id for subdept"
        else:
            tagged_user = get_object_or_None(User, id=tag_id)
            if tagged_user:
                notification_list.append(tagged_user)
                link_href = reverse("wall", kwargs={"wall_id" : tagged_user.erp_profile.wall.pk})
                my_text = my_text.replace('@' + tagged_user.first_name+"_"+tagged_user.last_name, link_text %(tagged_user.get_full_name(), link_href) )
            else:
                print "No id for user"
    return my_text, notification_list
    