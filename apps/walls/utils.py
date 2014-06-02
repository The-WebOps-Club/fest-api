# From Django
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext
from django.db.models import Q
from django.template.loader import render_to_string
from django.templatetags.static import static
from django.shortcuts import get_object_or_404
# Decorators
from django.contrib.auth.decorators import login_required, user_passes_test
# Python
from misc.utils import *  #Import miscellaneous functions
# From Apps
from apps.users.models import UserProfile, ERPProfile, Dept, Subdept, Page
from notifications.models import Notification
# Ajax post & comment
from apps.walls.models import Wall, Post, Comment
from apps.walls.permissions import PermissionStack, DEFAULT_POST_PERMISSION_STACK
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


def parse_atwho(my_text):
    """
        Parses through the list form atwho and records file, dept, subdept, user references.
    """
    notification_list = []
    
    #markdown_link_regex = re.compile("\[.*?\] \((.*?) \".*?\"\)", re.IGNORECASE) # need  to test this.
    markdown_link_regex = re.compile("\[([^\]]+)\]\(([^)\"]+)(?: \\\"([^\\\"]+)\\\")?\)", re.IGNORECASE)
    direct_link_regex = re.compile("data-notify=\\\"([^\\\"]+)\\\"", re.IGNORECASE)
    link_list = []
    link_list = markdown_link_regex.findall(my_text) + direct_link_regex.findall(my_text)

    for i in link_list:
        #data = link_list
        _type, _id = i[1].split("#", 1)
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
        elif _type == "page":
            notification_list.append(Page.objects.get(id=_id))

    return my_text, notification_list
    
def get_tag_object(tag):
    # `tags` Gives the first and last words after splitting with underscore.
    # First id and last is keyword (department, subdepartment and any others: email)
    if not isinstance(tag, list) and ( isinstance(tag, basestring) ):
        tag = tag.rsplit("_", 1)
    tag_id = int(tag[1])
    key = tag[0].lower()
    if key == "dept":
        obj = get_object_or_None(Dept, id=tag_id)
    elif key == "subdept":
        obj = get_object_or_None(Subdept, id=tag_id)
    elif key == "page":
        obj = get_object_or_None(Page, id=tag_id)
    else:
        obj = get_object_or_None(User, id=tag_id)
    return obj

def filter_objects(my_list):
    list_user = []
    list_subdept = []
    list_dept = []
    list_page = []
    for i in my_list:
        if isinstance(i, User):
            list_user.append(i)
        elif isinstance(i, ERPProfile):
            list_user.append(i.user)
        elif isinstance(i, Subdept):
            list_subdept.append(i)
        elif isinstance(i, Dept):
            list_dept.append(i)
        elif isinstance(i, Page):
            list_page.append(i)
    return list_user, list_subdept, list_dept, list_page

def query_newsfeed(user, **kwargs):
    """
        The query to get all notificatios related to a user
        This query clubs all notifications with the post's id and only which were sent to the user
    """
    page = kwargs.get("page", 0)
    max_items = kwargs.get("max_items", 5)
    if page and max_items:
        start_item = (page-1)*max_items
        end_item = page*max_items
    else:
        start_item = ""
        end_item = ""
    notification_query = """
            SELECT a.* 
            FROM notifications_notification a 
            WHERE ( ( NOT EXISTS (
                SELECT 1 
                FROM notifications_notification b
                WHERE b.target_object_id = a.target_object_id 
                    AND b.timestamp > a.timestamp
                    AND b.recipient_id=%(user_id)d
            ) ) AND a.recipient_id=%(user_id)d )
            GROUP BY a.target_object_id
            ORDER BY a.timestamp DESC
        """
    if start_item and end_item :
        notification_query += "LIMIT %(start_item)d,%(end_item)s"
    
    notification_query = notification_query % {"user_id" : user.id, 
        "start_item" : start_item, 
        "end_item" :  end_item,
    }
    notification_list = Notification.objects.raw(notification_query)
    return notification_list

def query_notifs(user, **kwargs):
    """
        The query to execute for notifs related to a user.
        This query clubs all notifications with the post's id and only which were sent to the user
    """
    notif_type = kwargs.get("notif_type", None)
    notif_unread = None
    if notif_type == "unread":
        notif_unread = 1
    elif notif_type == "read":
        notif_unread = 0
    page = kwargs.get("page", 0)
    max_items = kwargs.get("max_items", 5)
    if page and max_items:
        start_item = (page-1)*max_items
        end_item = page*max_items
    else:
        start_item = ""
        end_item = ""

    notif_query = """
            SELECT a.*
            FROM notifications_notification a 
            WHERE (a.recipient_id = %(user_id)s  
        """
    if notif_unread != None:
        notif_query += """AND a.unread = %(notif_unread)s """
    notif_query += """
            AND ( NOT EXISTS (
                SELECT 1 
                FROM notifications_notification b
                WHERE b.target_object_id = a.target_object_id 
                    AND b.timestamp > a.timestamp
                    AND b.recipient_id=%(user_id)d
            """
    if notif_unread != None:
        notif_query += """AND b.unread = %(notif_unread)s """
    notif_query += """
            ) ) )
            GROUP BY a.target_object_id 
            ORDER BY a.unread DESC, a.timestamp DESC
        """
    if start_item and end_item :
        notif_query += "LIMIT %(start_item)d,%(end_item)s"

    notif_query = notif_query.replace("\n", "") % { "user_id" : user.id, 
        "notif_unread" : notif_unread,
        "start_item" : start_item, 
        "end_item" :  end_item,
    }
    notif_list = Notification.objects.raw(notif_query)
    return notif_list


"""
    Old implementation of get_my_posts.
    Check below for the newer impelemetation
"""
def OLD_get_my_posts(access_obj, wall=None):
    """
        Checks all relations from a user to the posts in this wall
    """
    from apps.users.models import Dept, Subdept, Page

    if isinstance(access_obj, User):
        erp_profile = access_obj.erp_profile
        erp_coords = erp_profile.coord_relations.all()
        erp_supercoords = erp_profile.supercoord_relations.all()
        erp_cores = erp_profile.core_relations.all()
        erp_pages = erp_profile.page_relations.all()
        # directly given access to post
        # + have access to that wall
        my_query = ( \
                Q(access_users__id__exact=access_obj.id) | \
                Q(access_subdepts__in=erp_coords) | \
                Q(access_depts__in=erp_supercoords) | \
                Q(access_depts__in=erp_cores) | \
                Q(access_pages__in=erp_pages) | \
                Q(wall__access_users__id__exact=access_obj.id) | \
                Q(wall__access_subdepts__in=erp_coords) | \
                Q(wall__access_depts__in=erp_supercoords) | \
                Q(wall__access_depts__in=erp_cores) | \
                Q(wall__access_pages__in=erp_pages)
            )
        if wall:
            my_query = Q(wall=wall) & my_query
            if access_obj.is_superuser:
                my_query = Q(wall=wall)

        return Post.objects.filter(my_query).distinct().order_by('-time_created')
    elif isinstance(access_obj, Subdept) or isinstance(access_obj, Dept) or isinstance(access_obj, Page):
        temp = access_obj.access_post
        if wall:
            return temp.filter(wall=wall).distinct().order_by('-time_created')
        else:
            return temp.all().order_by('-time_created')

"""
    A newer get_my_posts designed on the PermissionStack class.
    Uses an already initialized PermissionStack instance to 
    build a query that retreives the Post objects significant
    to the user.
"""
def get_my_posts(access_obj, wall=None):

    from apps.users.models import Dept, Subdept, Page

    if isinstance(access_obj, User):
        
        stack = DEFAULT_POST_PERMISSION_STACK
        my_query = stack.get_filtered_query( access_obj, Post )

        if wall:
            my_query = Q(wall=wall) & my_query
            if access_obj.is_superuser:
                my_query = Q(wall=wall)

        return Post.objects.filter(my_query).distinct().order_by('-time_created')
    elif isinstance(access_obj, Subdept) or isinstance(access_obj, Dept) or isinstance(access_obj, Page):
        temp = access_obj.access_post
        if wall:
            return temp.filter(wall=wall).distinct().order_by('-time_created')
        else:
            return temp.all().order_by('-time_created')


def get_my_walls(user):
    """
        The query to get all walls related to a user
    """
    erp_profile = None
    if isinstance(user, User):
        user = user
        erp_profile = user.erp_profile
    elif isinstance(user, ERPProfile):
        erp_profile = user
        user = erp_profile.user
        
    erp_coords = erp_profile.coord_relations.all()
    erp_supercoords = erp_profile.supercoord_relations.all()
    erp_cores = erp_profile.core_relations.all()
    erp_pages = erp_profile.page_relations.all()
    # Direct relations 
    #   + All subdepts of my dept 
    #   + All depts related to my subdepts
    my_query = Q(person=erp_profile) | \
                Q(subdept__in=erp_coords) | \
                Q(dept__in=erp_supercoords) | \
                Q(dept__in=erp_cores) | \
                Q(page__in=erp_pages) | \
                Q(subdept__dept__in=erp_supercoords) | \
                Q(subdept__dept__in=erp_cores) | \
                Q(dept__subdepts__in=erp_coords)
                
    wall_list = Wall.objects.filter(my_query).distinct()
    return wall_list

def check_access_rights(access_obj, thing):
    """
        Used by walls and posts to check if the obj has access right or not
    """
    from apps.users.models import Dept, Subdept, Page
    if hasattr(thing, "person"): # Allow all user walls to be accessible by everyone
        return 1
    if isinstance(access_obj, User):
        erp_profile = access_obj.erp_profile
        erp_coords = erp_profile.coord_relations.all()
        erp_supercoords = erp_profile.supercoord_relations.all()
        erp_cores = erp_profile.core_relations.all()
        erp_pages = erp_profile.page_relations.all()
        
        # Have access to the thing directly
        id_query = Q(id=thing.id)
        my_query =  ( \
                Q(access_users__id__exact=access_obj.id) | \
                Q(access_subdepts__in=erp_coords) | \
                Q(access_depts__in=erp_supercoords) | \
                Q(access_depts__in=erp_cores) | \
                Q(access_pages__in=erp_pages)
            )
        if isinstance(thing, Post): 
            # + Access to the wall of this post
            # + wall is directly related to me
            #   + wall is related to all subdepts of my dept 
            #   + wall is related to all depts related to my subdepts
            my_query = my_query | \
                Q(wall__access_users__id__exact=access_obj.id) | \
                Q(wall__access_subdepts__in=erp_coords) | \
                Q(wall__access_depts__in=erp_supercoords) | \
                Q(wall__access_depts__in=erp_cores) | \
                Q(wall__access_pages__in=erp_pages) | \
                Q(wall__person=erp_profile) | \
                Q(wall__subdept__in=erp_coords) | \
                Q(wall__dept__in=erp_supercoords) | \
                Q(wall__dept__in=erp_cores) | \
                Q(wall__page__in=erp_pages) | \
                Q(wall__subdept__dept__in=erp_supercoords) | \
                Q(wall__subdept__dept__in=erp_cores) | \
                Q(wall__dept__subdepts__in=erp_coords)
            my_query = my_query & id_query
            return Post.objects.filter(my_query).distinct().count()
        elif isinstance(thing, Wall):
            # + Directly related to the wall
            #   + related to all subdepts of my dept 
            #   + related to all depts related to my subdepts
            my_query = my_query | \
                Q(person=erp_profile) | \
                Q(subdept__in=erp_coords) | \
                Q(dept__in=erp_supercoords) | \
                Q(dept__in=erp_cores) | \
                Q(page__in=erp_pages) | \
                Q(subdept__dept__in=erp_supercoords) | \
                Q(subdept__dept__in=erp_cores) | \
                Q(dept__subdepts__in=erp_coords)
            my_query = my_query & id_query
            return Wall.objects.filter(my_query).distinct().count()
    elif isinstance(access_obj, Subdept):
        return thing.access_subdepts.filter(id=access_obj.id).distinct().count()
    elif isinstance(access_obj, Dept):
        return thing.access_depts.filter(id=access_obj.id).distinct().count()
    elif isinstance(access_obj, Page):
        return thing.access_pages.filter(id=access_obj.id).distinct().count()

def check_admin_access_rights(access_obj, thing):
    from apps.users.models import Dept, Subdept, Page
    if isinstance(access_obj, User):
        #import pdb;pdb.set_trace()
        if (access_obj.is_superuser):
            return 1

        if( hasattr(thing,"page") and access_obj.is_staff ):
            return 1

        erp_profile = access_obj.erp_profile
        my_query = Q(id=thing.id) & ( \
                Q(wall__dept__in=erp_profile.supercoord_relations.all()) | \
                Q(wall__dept__in=erp_profile.core_relations.all()) | \
                Q(by__id = access_obj.id)
            )
        
        my_query = my_query 

        return Post.objects.filter( my_query ).distinct().count()




