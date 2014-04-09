"""
    Handles all signals related to users :
        ERPProfile pre_save
        Dept pre_save
        Subdept pre_save
"""
# Django
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.db.models import Q
# Apps
# Decorators
# Models
from apps.walls.models import Wall
from apps.events.models import Event
from apps.users.models import ERPProfile, Dept, Subdept
# Forms
# View functions
# Misc
from misc.utils import *
# Python
import datetime

def create_my_wall(item):
    """
        Create wall for an item and check name for (ERPProfile, Dept or Subdept) associated to the wall

        Args:
            item - An item of type (ERPProfile, Dept or Subdept)
    """
    # Validate arguments
    changed_it = False
    if not ( type(item) is ERPProfile or type(item) is Dept or type(item) is Subdept ):
        raise InvalidArgumentTypeException
    
    # Check if wall exists. If not, create. If it does, check name
    if hasattr(item, "wall"):
        if item.wall.name != item.name: # Check if name changed
            item.wall.name = item.name
            changed_it = True
    else: # Create a new wall
        item.wall = Wall.objects.create(name=item.name)
        changed_it = True

    if changed_it:
        item.wall.save()
        

def associate_to_wall(item):
    """
        Associate the item to a wall
            - Associate the item (ERPProfile, Dept or Subdept) to it's wall to make the user an owner, add for notifs and reading rights

        Args:
            item - An item of type (ERPProfile, Dept or Subdept)
    """
    # Validate arguments
    changed_it = False
    if not ( type(item) is ERPProfile or type(item) is Dept or type(item) is Subdept ):
        raise InvalidArgumentTypeException
    
    # Set the notifications correctly if not correct
    if type(item) is ERPProfile:
        add_items = [item.user]
    elif type(item) is Dept or type(item) is Subdept:
        add_items = item.related_users()
    
    print add_items
    if hasattr(item.wall, "notification_users") and item not in item.wall.notification_users.all():
        item.wall.notification_users.add(*add_items)
        changed_it = True
        print "Added", add_items, "into notif list of the wall", item.wall.name
    if hasattr(item.wall, "notification_users") and item not in item.wall.owners.all():
        item.wall.owners.add(*add_items)
        changed_it = True
        print "Added", add_items, "into owner list of the wall", item.wall.name
    if hasattr(item.wall, "notification_users") and item not in item.wall.visible_to.all():
        item.wall.visible_to.add(*add_items)
        changed_it = True
        print "Added", add_items, "into visible list of the wall", item.wall.name
        
    if changed_it:
        item.wall.save()

# ----------------------------------------------------------------------------------
# ------------------------- ERP PROFILE

@receiver(pre_save, sender=ERPProfile, dispatch_uid="erpprofile.made.pre_save_signal")
def erpprofile_pre_save(sender, instance, **kwargs):
    create_my_wall(instance)

@receiver(post_save, sender=ERPProfile, dispatch_uid="erpprofile.made.post_save_signal")
def erpprofile_post_save(sender, instance, **kwargs):
    associate_to_wall(instance)

# ----------------------------------------------------------------------------------
# ------------------------- DEPT

@receiver(pre_save, sender=Dept, dispatch_uid="dept.made.pre_save_signal")
def dept_pre_save(sender, instance, **kwargs):
    create_my_wall(instance)

@receiver(post_save, sender=Dept, dispatch_uid="dept.made.post_save_signal")
def dept_post_save(sender, instance, **kwargs):
    associate_to_wall(instance)

# ----------------------------------------------------------------------------------
# ------------------------- SUB DEPT

@receiver(pre_save, sender=Subdept, dispatch_uid="subdept.made.pre_save_signal")
def subdept_pre_save(sender, instance, **kwargs):
    create_my_wall(instance)

@receiver(post_save, sender=Subdept, dispatch_uid="subdept.made.post_save_signal")
def subdept_post_save(sender, instance, **kwargs):
    associate_to_wall(instance)
