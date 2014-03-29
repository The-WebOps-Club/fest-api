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
# Apps
from notifications import notify
# Decorators
# Models
# Forms
# View functions
# Misc
from misc.utils import *
# Python
import random

# Model for Department forum
class Wall(models.Model):
    """
        Defines a Wall - a wall can be of a person, department or subdepartment
        It is linked using a OneToOne field on the side of the Person, Department or SubDepartment
        
        @todo : Add analytics to be able to see when each person saw the wall last
    """
    
    # Basic information
    name                = models.CharField(max_length=60, unique=True)
    
    # Relations with other models
    # Owners can view all the posts and make posts, For a department they are the Department Junta
    owners              = models.ManyToManyField(User, null=True, blank=True, related_name='walls') # People who get notifications about this wall
    notification_users  = models.ManyToManyField(User, null=True, blank=True, related_name='notified_wall')
    visible_to          = models.ManyToManyField(User, null=True, blank=True, related_name='visible_wall')
    # Analytics


    def save(self, *args, **kwargs):
        """
            An extended save method to handle   
                - M2M associated with the model
                - Add all the owners to notification and visible_to 
        """

        temp = super(Post, self).save(*args, **kwargs)
        return

    @property
    def parent(self):
        temp = None
        try : temp = self.person()
        except AttributeError as ae2: 
            try : temp = self.dept()
            except AttributeError as ae2: 
                try : temp = self.subdept()
                except AttributeError as ae3: 
                    temp = None
            
        return temp
    
    def __unicode__(self):
        return self.name
    
class PostInfo(models.Model):
    """
        Defines the PostInfo class. The model which has some kind of data about a message.
        Used for both Post and Comment
        @todo : Add options to upload a file to any message
    """
    # Basic data
    description     = models.TextField(blank=True, default='') # The matter of post
    by              = models.ForeignKey(User, related_name='posts_created')

    # Analytics
    time_created    = models.DateTimeField(auto_now_add=True)
    time_updated    = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        LIMIT = 50
        tail = len(self.description) > LIMIT and '...' or ''
        return self.description[:LIMIT] + tail

    class Meta:
        abstract = True
        ordering = ['time_created']
        get_latest_by = 'time_created'

    def __unicode__(self):
        return self.description

class Comment(PostInfo):
    """
        Defines the comment to a Post
    """
    def __unicode__(self):
        return self.description

class Post(PostInfo):
    """
        Defines the Post Class. Holds data about each post made on a Wall.
    """
    wall                = models.ForeignKey(Wall, related_name='posts', blank = True, null = True)
    notification_users  = models.ManyToManyField(User, null=True, blank=True, related_name='notified_post')
    visible_to          = models.ManyToManyField(User, null=True, blank=True, related_name='visible_post')
    is_public           = models.BooleanField(default=True)
    comments            = models.ManyToManyField(Comment, null=True, blank=True, related_name='parent_post')
    comments_count      = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        """
            An extended save method to handle   
                - M2M associated with the model
                - Add all the 
        """
        
        temp = super(Post, self).save(*args, **kwargs)
        return


@receiver(post_save, sender=Post, dispatch_uid="post.made.signal")
def notify_post(sender, instance, **kwargs):
    """
        Signal for  : A Post got saved on a wall
        Creates     : Notification to correspinding notification_users on wall.
    """
    # If comments = 0 It is a new post.
    if not comments_count:
        for recipient in instance.wall.notification_users:
            notify.send(
                sender=instance.by, recipient=recipient,
                verb='has posted on', action_object=instance, target=instance.wall
            )

@receiver(post_save, sender=Comment, dispatch_uid="comment.made.signal")
def notify_comment(sender, instance, **kwargs):
    """
        Signal for  : A Comment got saved on a post
        Creates     : Notification to correspinding notification_users on Post.
    """
    for recipient in instance.parent_post.notification_users:
        notify.send(
            sender=instance.by, recipient=recipient,
            verb='has commented on', action_object=instance, target=instance.parent_post
        )