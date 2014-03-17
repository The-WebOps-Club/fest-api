"""
    Handles all models related to users :
        - College : Name, city and state of a college 

"""
# Django
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
# Apps
# Decorators
# Models
# Forms
# View functions
# Misc
from misc.utils import *  #Import miscellaneous functions
from misc.constants import *
# Python
import datetime
 
class College(models.Model):

    name = models.CharField(max_length=255)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=40, choices=STATE_CHOICES)

    def __unicode__(self):
        return '%s, %s, %s' % (self.name, self.city, self.state)

    class Admin:
        pass



