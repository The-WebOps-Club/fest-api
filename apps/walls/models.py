"""
    Handles all models related to walls :
        - Wall : The general model declaring everything inside a class
        - Post : The basic fucntioning unit of a Wall - Posts. 

"""
# Django
from django.db import models
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
        print "No parent found"
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

    def notify_users(self):
        users = set()
        users.update(self.notification_users.all())
        for dept in self.notification_depts.all():
            users.update(dept.related_users())
        for sub_dept in self.notification_subdepts.all():
            users.update(sub_dept.related_users())
        for page in self.notification_pages.all():
            users.update(page.related_users())
        return users
    
    def __unicode__(self):
        return self.name

class PostInfo(models.Model):
    """
        Defines the PostInfo class. The model which has some kind of data about a message.
        Used for both Post and Comment
        @todo : Add options to upload a file to any message
    """
    is_active       = models.BooleanField(default=True)

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

    def send_notif(self, notif_list=None):
        # Had to do this because signals refuse to work.
        parent_post = self.parent_post.first() # There is only one parent_post
        parent_wall = parent_post.wall
        if not notif_list:
            notif_list  = parent_post.notify_users() # Get post notifs
            notif_list.update(parent_wall.notify_users()) # Get my wall notifs
        for recipient in notif_list:
            # Check if receipient already has notif on this parent_post
            curr_notif = get_object_or_None(recipient.notifications.unread(), target_object_id=parent_post.id)
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
                    target=parent_post, # The model which got affected - POST
                    # In case you wish to get the wall on which it hapened, use target.wall (this is to ensure uniformity in all notifications)
                    description = 'wall:'+format(parent_wall.pk),
                )



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

    def notify_users(self):
        users = set()
        users.update(self.notification_users.all())
        for dept in self.notification_depts.all():
            users.update(dept.related_users())
        for sub_dept in self.notification_subdepts.all():
            users.update(sub_dept.related_users())
        for page in self.notification_pages.all():
            users.update(page.related_users())
        return users

    def send_notif(self, notif_list=None):
        # Had to do this because signals refuse to work.
        if not notif_list:
            notif_list  = self.notify_users() # Get my notifs
            notif_list.update(self.wall.notify_users()) # Get my wall notifs
        for recipient in notif_list:
            # Check if receipient already has notif on this post
            curr_notif = get_object_or_None(recipient.notifications.unread(), target_object_id=self.id)
            if curr_notif:
                curr_notif.mark_as_read()
            by = self.by
            if recipient != by:
                notifications.notify.send(
                    sender=by, # The model who wrote the post - USER
                    recipient=recipient, # The model who sees the post - USER
                    verb='has posted on', # verb
                    action_object=self, # the model on which something happened - POST
                    target=self, # The model which got affected - POST
                    description = 'wall:'+format(self.wall.pk),
                    # In case you wish to get the wall on which it hapened, use target.wall (this is to ensure uniformity in all notifications)
                )

    def get_absolute_url(self):
        post_str = '#post_' + str(self.pk)
        return reverse('apps.walls.views.wall', args=(self.wall.pk,)) + post_str
        
    class Meta:
        get_latest_by = 'time_created'
