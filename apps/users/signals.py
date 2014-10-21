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
from apps.users.models import ERPProfile, Dept, Subdept, Page
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
    if not ( type(item) is ERPProfile or type(item) is Dept or type(item) is Subdept or type(item) is Page ):
        raise InvalidArgumentTypeException
    
    # Check if wall exists. If not, create. If it does, check name
    if hasattr(item, "wall"):
        if item.wall.name != item.name: # Check if name changed
            item.wall.name = item.name
            changed_it = True
    else: # Create a new wall
        from apps.walls.models import Wall
        item.wall = Wall.objects.create(name=item.name)
        changed_it = True

    if changed_it:
        item.wall.save()
        
# ----------------------------------------------------------------------------------
# ------------------------- ERP PROFILE

@receiver(pre_save, sender=ERPProfile, dispatch_uid="erpprofile.made.pre_save_signal")
def erpprofile_pre_save(sender, instance, **kwargs):
    create_my_wall(instance)

@receiver(post_save, sender=ERPProfile, dispatch_uid="erpprofile.made.post_save_signal")
def erpprofile_post_save(sender, instance, **kwargs):
    instance.wall.add_notifications([instance.user])

# ----------------------------------------------------------------------------------
# ------------------------- DEPT

@receiver(pre_save, sender=Dept, dispatch_uid="dept.made.pre_save_signal")
def dept_pre_save(sender, instance, **kwargs):
    create_my_wall(instance)

@receiver(post_save, sender=Dept, dispatch_uid="dept.made.post_save_signal")
def dept_post_save(sender, instance, **kwargs):
    instance.wall.add_notifications([instance])

# ----------------------------------------------------------------------------------
# ------------------------- SUB DEPT

@receiver(pre_save, sender=Subdept, dispatch_uid="subdept.made.pre_save_signal")
def subdept_pre_save(sender, instance, **kwargs):
    create_my_wall(instance)

@receiver(post_save, sender=Subdept, dispatch_uid="subdept.made.post_save_signal")
def subdept_post_save(sender, instance, **kwargs):
    instance.wall.add_notifications([instance])

# ----------------------------------------------------------------------------------
# ------------------------- PAGE

@receiver(pre_save, sender=Page, dispatch_uid="page.made.pre_save_signal")
def page_pre_save(sender, instance, **kwargs):
    create_my_wall(instance)

@receiver(post_save, sender=Page, dispatch_uid="page.made.post_save_signal")
def page_post_save(sender, instance, **kwargs):
    instance.wall.add_notifications([instance])
