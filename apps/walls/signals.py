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

@receiver(post_save, sender=Post, dispatch_uid="post.made.post_save_signal")
def post_post_save(sender, instance, **kwargs):
    """
        Signal for  : A Post got saved on a wall
        Creates     : Notification to correspinding notification_users on wall.
    """
    # If comments = 0 It is a new post.
    if not instance.comments_count:
        for recipient in instance.wall.notification_users.all():
            notify.send(
                sender=instance.by, recipient=recipient,
                verb='has posted on', action_object=instance, target=instance.wall
            )

@receiver(post_save, sender=Comment, dispatch_uid="comment.made.post_save_signal")
def comment_post_save(sender, instance, **kwargs):
    """
        Signal for  : A Comment got saved on a post
        Creates     : Notification to correspinding notification_users on Post.
    """
    for recipient in instance.parent_post.all():
        notify.send(
            sender=instance.by, recipient=recipient,
            verb='has commented on', action_object=instance, target=instance.parent_post
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
