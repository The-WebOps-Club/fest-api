"""
    Handles all signals related to users :
        ERPProfile post_save
        Dept post_save
        Subdept post_save
"""
# Django
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, m2m_changed
# Apps
# Decorators
# Models
from apps.walls.models import Wall, Post, Comment
# Forms
# View functions
# Misc
from misc.utils import *
# Python
import notifications

@receiver(post_save, sender=Post, dispatch_uid="post.made.post_save_signal")
def post_post_save(sender, instance, created, **kwargs):
    """
        Signal for  : A Post got saved on a wall
        Creates     : Notification to correspinding notification_users on wall.
    """
    # If comments = 0 It is a new post.
    if created:
        for recipient in instance.wall.notification_users.all():
            notifications.notify.send(
                sender=instance.by, # The model who wrote the post - USER
                recipient=recipient, # The model who sees the post - USER
                verb='has posted on', # verb
                action_object=instance, # the model on which something happened - POST
                target=instance # The model which got affected - POST
                # In case you wish to get the wall on which it hapened, use target.wall (this is to ensure uniformity in all notifications)
            )

@receiver(m2m_changed, sender=Post.comments.through, dispatch_uid="post.made.m2m_changed_signal")
def post_m2m_changed(sender, instance, action, reverse, model, pk_set, using, **kwargs):
    """
        Signal for  : A Comment got saved on a post
        Creates     : Notification to correspinding notification_users on Post.
    """
    if action == "post_add" :
    	for recipient in instance.wall.notification_users.all():
	        notifications.notify.send(
	            sender=instance.by, # The model who wrote the post - USER
	            recipient=recipient, # The model who sees the post - USER
	            verb='has commented on', # verb
	            action_object=model.objects.get(pk = list(pk_set)[0]), # the model on which something happened - COMMENT
	            target=instance # The model which got affected - POST
	            # In case you wish to get the wall on which it hapened, use target.wall (this is to ensure uniformity in all notifications)
	        )

# @receiver(m2m_changed, sender=Wall., dispatch_uid="wall.made.m2m_changed_signal")
# def wall_m2m_changed(sender, instance, **kwargs):
#     """
#         Signal for  : A Comment got saved on a post
#         Creates     : Notification to correspinding notification_users on Post.
#     """
#     for recipient in instance.parent_post.all():
#         notify.send(
#             sender=instance.by, recipient=recipient,
#             verb='has commented on', action_object=instance, target=instance.parent_post
#         )
