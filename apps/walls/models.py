"""
    Handles all models related to walls :
        - Wall : The general model declaring everything inside a class
        - Post : The basic fucntioning unit of a Wall - Posts. 

"""
# Django
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.signals import request_finished
from django.core.urlresolvers import reverse
# Apps
# Decorators
# Models
#from misc.managers import CheckActiveManager
# Forms
# View functions
# Misc
from misc.utils import *
from annoying.functions import get_object_or_None
import notifications
# Python
import random

#### MODELS

# Model for Department forum
class Wall(models.Model):
    """
        Defines a Wall - a wall can be of a person, department or subdepartment
        It is linked using a OneToOne field on the side of the Person, Department or SubDepartment
        
        @todo : Add analytics to be able to see when each person saw the wall last
    """
    is_active       = models.BooleanField(default=True)
    is_public       = models.BooleanField(default=False)
    
    # Basic information
    name                 = models.CharField(max_length=60)
    
    # Relations with other models
    notification_users   = models.ManyToManyField(User, null=True, blank=True, related_name='notified_wall')
    notification_subdepts= models.ManyToManyField('users.Subdept', null=True, blank=True, related_name='notified_wall')
    notification_depts   = models.ManyToManyField('users.Dept', null=True, blank=True, related_name='notified_wall')
    notification_pages   = models.ManyToManyField('users.Page', null=True, blank=True, related_name='notified_wall')
    
    access_users   = models.ManyToManyField(User, null=True, blank=True, related_name='access_wall')
    access_subdepts= models.ManyToManyField('users.Subdept', null=True, blank=True, related_name='access_wall')
    access_depts   = models.ManyToManyField('users.Dept', null=True, blank=True, related_name='access_wall')
    access_pages   = models.ManyToManyField('users.Page', null=True, blank=True, related_name='access_wall')
    access_public  = models.BooleanField(default=False)
    
    # Analytics
    # seen_user            = models.ManyToManyField(User, null=True, blank=True, related_name='seen_wall', through=UserWall)
    time_updated    = models.DateTimeField(auto_now=True, default = datetime.datetime(1950, 1, 1))
    cache_updated   = models.DateTimeField(auto_now=True, default = datetime.datetime(1950, 1, 1))
    
    objects = CheckActiveManager()
    
    def save(self, *args, **kwargs):
        """
            An extended save method to handle   
                - M2M associated with the model
                - Add all the owners to notification and visible_to 
        """

        temp = super(Wall, self).save(*args, **kwargs)
        return

    @property
    def parent(self):
        temp = None
        if hasattr(self, "person"): # User
            return self.person.user
        elif hasattr(self, "subdept"): # Subdept
            return self.subdept
        elif hasattr(self, "dept"): # Dept
            return self.dept
        elif hasattr(self, "page"): # Dept
            return self.page
        return temp
    
    def has_access(self, access_obj):
        from apps.walls.utils import check_access_rights
        return check_access_rights(access_obj, self)

    def add_access(self, access_list):
        from apps.walls.utils import filter_objects
        list_user, list_subdept, list_dept, list_page = filter_objects(access_list)
        self.access_users.add(*list_user)
        self.access_subdepts.add(*list_subdept)
        self.access_depts.add(*list_dept)
        self.access_pages.add(*list_page)
    
    def add_notifications(self, notif_list):
        from apps.walls.utils import filter_objects
        list_user, list_subdept, list_dept, list_page = filter_objects(notif_list)
        self.notification_users.add(*list_user)
        self.notification_subdepts.add(*list_subdept)
        self.notification_depts.add(*list_dept)
        self.notification_pages.add(*list_page)
        self.add_access(notif_list) # This is so that they can read and comment also ...

    def notify_users_query(self):
        notif_depts = self.notification_depts.all()
        notif_subdepts = self.notification_subdepts.all()
        notif_pages = self.notification_pages.all()
        query = ( \
            Q(id__in=self.notification_users.values_list('id', flat=True)) | \
            Q(erp_profile__page_relations__in=notif_pages) | \
            Q(erp_profile__core_relations__in=notif_depts) | \
            Q(erp_profile__supercoord_relations__in=notif_depts) | \
            Q(erp_profile__coord_relations__in=notif_subdepts) 
        )
        return query
        
    def notify_users(self):
        return User.objects.filter( self.notiy_users_query() )
    
    def __unicode__(self):
        return self.name

class PostInfo(models.Model):
    """
        Defines the PostInfo class. The model which has some kind of data about a message.
        Used for both Post and Comment
        @todo : Add options to upload a file to any message
    """
    is_active       = models.BooleanField(default=True)
    is_public       = models.BooleanField(default=False)
    
    # Basic data
    description     = models.TextField(blank=True, default='') # The matter of post
    by              = models.ForeignKey(User, related_name='%(class)s_created')

    # Analytics
    time_created    = models.DateTimeField(auto_now_add=True)
    time_updated    = models.DateTimeField(auto_now=True)
    
    objects = CheckActiveManager()
    
    def __unicode__(self):
        LIMIT = 50
        tail = len(self.description) > LIMIT and '...' or ''
        return self.description[:LIMIT] + tail

    def send_notif(self, notif_list=None):
        # Had to do this because signals refuse to work.
        if isinstance(self, Post):
            post = self
            notif_verb = "has posted on"
        elif isinstance(self, Comment):
            post = self.parent_post.all()[0] # There is only one parent_post
            notif_verb = "has commented on"
        wall = post.wall
        if not notif_list:
            # Get my wall and posts which I am to get notifs for
            notif_list  = User.objects.filter(post.notify_users_query() | wall.notify_users_query())
        for recipient in notif_list:
            # Check if receipient already has notif on this post
            curr_notif = get_object_or_None(recipient.notifications.unread(), target_object_id=post.id)
            if curr_notif:
                curr_notif.mark_as_read()
            by = self.by
            # Now create a new unread notif
            if recipient != by:
                notifications.notify.send(
                    sender=by, # The model who wrote the post - USER
                    recipient=recipient, # The model who sees the post - USER
                    verb='has commented on', # verb
                    action_object=self, # the model on which something happened - POST
                    target=post, # The model which got affected - POST
                    # In case you wish to get the wall on which it hapened, use target.wall (this is to ensure uniformity in all notifications)
                    description = 'wall:' + str(wall.pk),
                )

    class Meta:
        abstract = True
        ordering = ['time_created']
        get_latest_by = 'time_created'

class Comment(PostInfo):
    """
        Defines the comment to a Post
    """
    liked_users  = models.ManyToManyField(User, null=True, blank=True, related_name='liked_comment')

    def __unicode__(self):
        return self.description

    class Meta:
        get_latest_by = 'time_created'

    


class Post(PostInfo):
    """
        Defines the Post Class. Holds data about each post made on a Wall.
    """
    subject             = models.CharField(max_length=200, blank=True, null=True)
    # Relations with other models - Wall
    wall                = models.ForeignKey(Wall, related_name='posts', blank = True, null = True)
    
    # Relations with other models - Users
    notification_users  = models.ManyToManyField(User, null=True, blank=True, related_name='notified_post')
    notification_depts  = models.ManyToManyField('users.Dept', null=True, blank=True, related_name='notified_post')
    notification_subdepts= models.ManyToManyField('users.Subdept', null=True, blank=True, related_name='notified_post')
    notification_pages  = models.ManyToManyField('users.Page', null=True, blank=True, related_name='notified_post')

    access_users   = models.ManyToManyField(User, null=True, blank=True, related_name='access_post')
    access_subdepts= models.ManyToManyField('users.Subdept', null=True, blank=True, related_name='access_post')
    access_depts   = models.ManyToManyField('users.Dept', null=True, blank=True, related_name='access_post')
    access_pages   = models.ManyToManyField('users.Page', null=True, blank=True, related_name='access_post')
    access_public  = models.BooleanField(default=False)

    liked_users  = models.ManyToManyField(User, null=True, blank=True, related_name='liked_post')

    # Relations with other models - Comments
    comments            = models.ManyToManyField(Comment, null=True, blank=True, related_name='parent_post')
    comments_count      = models.IntegerField(default=0)

    # Analytics
    # seen_user       = models.ManyToManyField(User, null=True, blank=True, related_name='seen_post', through=UserPost)


    def save(self, *args, **kwargs):
        """
            An extended save method to handle   
                - M2M associated with the model
                - Add all the   
        """
        
        temp = super(Post, self).save(*args, **kwargs)
        return

    def has_access(self, access_obj):
        from apps.walls.utils import check_access_rights
        check_access_rights(access_obj, self)
        
    def add_access(self, access_list):
        from apps.walls.utils import filter_objects
        list_user, list_subdept, list_dept, list_page = filter_objects(access_list)
        self.access_users.add(*list_user)
        self.access_subdepts.add(*list_subdept)
        self.access_depts.add(*list_dept)
        self.access_pages.add(*list_page)
    
    def add_notifications(self, notif_list):
        from apps.walls.utils import filter_objects
        list_user, list_subdept, list_dept, list_page = filter_objects(notif_list)
        self.notification_users.add(*list_user)
        self.notification_subdepts.add(*list_subdept)
        self.notification_depts.add(*list_dept)
        self.notification_pages.add(*list_page)
        self.add_access(notif_list) # This is so that they can read and comment also ...

    def notify_users_query(self):
        notif_depts = self.notification_depts.all()
        notif_subdepts = self.notification_subdepts.all()
        notif_pages = self.notification_pages.all()
        query = ( \
            Q(id__in=self.notification_users.values_list('id', flat=True)) | \
            Q(erp_profile__page_relations__in=notif_pages) | \
            Q(erp_profile__core_relations__in=notif_depts) | \
            Q(erp_profile__supercoord_relations__in=notif_depts) | \
            Q(erp_profile__coord_relations__in=notif_subdepts) 
        )
        return query
        
    def notify_users(self):
        return User.objects.filter( self.notiy_users_query() )
        
    def get_absolute_url(self):
        post_str = '#post_' + str(self.pk)
        return reverse('apps.walls.views.wall', args=(self.wall.pk,)) + post_str
        
    class Meta:
        get_latest_by = 'time_created'
