"""
    Handles all models related to users :
        - User Profile : Handles the basic information of people, their college, their fest related information
        - ERPUser : Handles the information of a users organizational role

"""
# Django
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
# Apps
# Decorators
# Models
from misc.models import College
# Forms
# View functions
# Misc
from misc.utils import *
from misc.constants import *
# Python
import datetime


class UserProfile(models.Model): # The corresponding auth user
    """
        The model is a basic model for any user who will come into Shaastra.
        
        It handles the basic 
    
    """
    user               = models.ForeignKey(User, unique=True)
    
    # Basic information
    gender             = models.CharField(max_length=1, choices=GENDER_CHOICES, default='F')
    age                = models.IntegerField(default=18)
    mobile_number      = models.CharField(max_length=15, blank=True, null=True, help_text='Please enter your current mobile number')
    
    # College info
    branch             = models.CharField(max_length=50, choices=BRANCH_CHOICES, help_text='Your branch of study')
    college            = models.ForeignKey(College, null=True, blank=True)
    college_roll       = models.CharField(max_length=40, null=True)
    school_student     = models.BooleanField(default=False)
    
    # Fest related info
    want_accomodation  = models.BooleanField(default=False, help_text = "Doesn't assure accommodation.")
    
    activation_key     = models.CharField(max_length=40, null=True)
    key_expires        = models.DateTimeField(default=timezone.now() + datetime.timedelta(2))
    is_core            = models.BooleanField(default=False)
    is_hospi           = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        #self.user.save()
        super(UserProfile, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        self.user.delete()
        super(UserProfile, self).delete(*args, **kwargs)
    
    def __unicode__(self):
        return self.user.first_name
    
    class Admin:
        pass

class ERPUser(models.Model):
    user = models.OneToOneField(User) # The corresponding auth user
    
    # Temporary role in the Fest after selecting which identity he is
    dept = models.ForeignKey(Dept, related_name='dept_user_set')
    subdept = models.ForeignKey(Subdept, blank=True, null=True, default=None, related_name='subdept_user_set')
    level = models.IntegerField(default=0) # 0 = Coord, 1 = Supercoord, 2 = Core
    
    # event = models.ForeignKey(GenericEvent, null=True, blank=True)
    
    # Shaastra Relations - all possible roles in the fest
    coord_relations = models.ManyToManyField(Subdept, null=True, blank=True, related_name='coord_set')
    supercoord_relations = models.ManyToManyField(Dept, null=True, blank=True, related_name='supercoord_set')
    core_relations = models.ManyToManyField(Dept, null=True, blank=True, related_name='core_set')
    
    # Other random information for profile
    nickname = models.CharField(max_length=100, blank=True, null=True)
    room_no = models.IntegerField(default=0, blank=True, null=True )
    hostel = models.CharField(max_length=15, choices = HOSTEL_CHOICES, blank=True, null=True)
    chennai_number = models.CharField(max_length=15, blank=True, null=True)
    summer_number = models.CharField(max_length=15, blank=True, null=True)
    
    # Holiday stay
    summer_stay = models.CharField(max_length=30, blank=True, null=True)
    winter_stay = models.CharField(max_length=30, blank=True, null=True)
    
    def __unicode__(self):
        return self.user.first_name + ' ' + self.user.last_name
    
    # Methods to check for position/role
    def is_coord(self):
        return self.level == 0
    def is_supercoord(self):
        return self.level == 1
    def is_core(self):
        return self.level == 2
    def get_position (self):
        """ Gives verbose name for level """
        if self.level == 2:
            return 'Core'
        if self.level == 1:
            return 'Supercoord'
        if self.level == 0:
            return 'Coord'
    def get_dept_subdept(self):
        """ Dept (subdept)"""
        dept_str = self.dept.name
        if self.subdept:
            dept_str += " (" + self.subdept.name + ")"
        return dept_str
    
    def __unicode__(self):
        return self.user.first_name
        
# Department Models
class Dept(models.Model):
    name = models.CharField(max_length=30)
    
    def __unicode__(self):
        return self.name	


class Subdept(models.Model):
    """ Every subdept is linked to an event """
    dept = models.ForeignKey(Dept)
    
    name = models.CharField(max_length=30)
    event = models.ForeignKey(GenericEvent, null=True, blank=True)
    
    def __unicode__(self):
        return self.name

