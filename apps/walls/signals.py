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
from annoying.functions import get_object_or_None
# Python
import notifications

# @receiver(post_save, sender=Post, dispatch_uid="post.made.post_save_signal")
# def post_post_save(sender, instance, created, **kwargs):
#     """
#         Signal for  : A Post got saved on a wall
#         Creates     : Notification to correspinding notification_users on wall.
#     """
#     # If comments = 0 It is a new post.
#     if created:
#         by = instance.by
#         set_recipients = set()
#         set_recipients.update(instance.wall.notify_users())
#         set_recipients.update(instance.notify_users())
#         for recipient in list(set_recipients):
#             curr_notif = get_object_or_None(recipient.notifications.unread(), target_object_id=instance.id)
#             if curr_notif:
#                 curr_notif.mark_as_read()
#             if recipient != by:
#                 notifications.notify.send(
#                     sender=by, # The model who wrote the post - USER
#                     recipient=recipient, # The model who sees the post - USER
#                     verb='has posted on', # verb
#                     action_object=instance, # the model on which something happened - POST
#                     target=instance # The model which got affected - POST
#                     # In case you wish to get the wall on which it hapened, use target.wall (this is to ensure uniformity in all notifications)
#                 )

# @receiver(m2m_changed, sender=Post.comments.through, dispatch_uid="post.made.m2m_changed_signal")
# def post_m2m_changed(sender, instance, action, reverse, model, pk_set, using, **kwargs):
#     """
#         Signal for  : A Comment got saved on a post
#         Creates     : Notification to corresponding notification_users on Post.
#     """
#     if action == "post_add" :
#         by = instance.comments.last().by
#         set_recipients = set()
#         set_recipients.update(instance.wall.notify_users())
#         set_recipients.update(instance.notify_users())
#     	for recipient in list(set_recipients):
#             curr_notif = get_object_or_None(recipient.notifications.unread(), target_object_id=instance.id)
#             if curr_notif:
#                 curr_notif.mark_as_read()
#             if recipient != by:
#     	        notifications.notify.send(
#     	            sender= by, # The model who wrote the post - USER
#     	            recipient=recipient, # The model who sees the post - USER
#     	            verb='has commented on', # verb
#     	            action_object=model.objects.get(pk = list(pk_set)[0]), # the model on which something happened - COMMENT
#     	            target=instance, # The model which got affected - POST
#        	            # In case you wish to get the wall on which it hapened, use target.wall (this is to ensure uniformity in all notifications)
#     	        )

# @receiver(m2m_changed, sender=Post.notification_depts.through, dispatch_uid="depts.made.m2m_changed_signal")
# def dept_m2m_changed(sender, instance, action, reverse, model, pk_set, using, **kwargs):
#     """
#         Signal for  : A Dept added to a post
#         Creates     : Notification to corresponding users part of notification_depts on Post.
#     """
#     if action == "post_add" :
#         if(instance.comments.last()):
#             by = instance.comments.last().by
#         else:
#         	by = instance.by    
#         set_recipients = set()
#         set_recipients.update(instance.wall.notify_users())
#         set_recipients.update(instance.notify_users())
#     	for recipient in list(set_recipients):
#             curr_notif = get_object_or_None(recipient.notifications.unread(), target_object_id=instance.id)
#             if curr_notif:
#                 curr_notif.mark_as_read()
#             if recipient != by:
#     	        notifications.notify.send(
#     	            sender= by, # The model who wrote the post - USER
#     	            recipient=recipient, # The model who sees the post - USER
#     	            verb='has commented on', # verb
#     	            # TODO: @Ali -Changed action_object from model.objects.get(pk = list(pk_set)[0]), please check if this affects 						anything you did before
#     	            action_object=instance.comments.last(), # the model on which something happened - COMMENT
#     	            target=instance, # The model which got affected - POST
#        	            # In case you wish to get the wall on which it hapened, use target.wall (this is to ensure uniformity in all notifications)
#     	        )
    	        
# @receiver(m2m_changed, sender=Post.notification_subdepts.through, dispatch_uid="subdepts.made.m2m_changed_signal")
# def subdept_m2m_changed(sender, instance, action, reverse, model, pk_set, using, **kwargs):
#     """
#         Signal for  : A Dept added to a post
#         Creates     : Notification to corresponding users part of notification_subdepts on Post.
#     """
#     if action == "post_add" :
#         if(instance.comments.last()):
#             by = instance.comments.last().by
#         else:
#         	by = instance.by    
#         set_recipients = set()
#         set_recipients.update(instance.wall.notify_users())
#         set_recipients.update(instance.notify_users())
#     	for recipient in list(set_recipients):
#             curr_notif = get_object_or_None(recipient.notifications.unread(), target_object_id=instance.id)
#             if curr_notif:
#                 curr_notif.mark_as_read()
#             if recipient != by:
#     	        notifications.notify.send(
#     	            sender= by, # The model who wrote the post - USER
#     	            recipient=recipient, # The model who sees the post - USER
#     	            verb='has commented on', # verb
#     	            action_object=instance.comments.last(), # the model on which something happened - COMMENT
#     	            target=instance, # The model which got affected - POST
#        	            # In case you wish to get the wall on which it hapened, use target.wall (this is to ensure uniformity in all notifications)
#     	        )

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
