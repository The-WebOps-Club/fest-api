"""
    Handles all models related to events :
        - Event : Information abotu an event in shaastra

"""
# Django
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Apps
# Decorators
# Models
from apps.walls.models import Wall, Post
from apps.users.models import User
# Forms
# View functions
# Misc
from misc.utils import *
# Python
"""
class Event(models.Model):
    CATEGORY_CHOICES = (
        ('Onsite', 'Onsite'),
        ('Online', 'Online'),
        ('Pre-registered', 'Pre registered'),
    )
    
    name = models.CharField(max_length=50)
    oneliner = models.CharField(max_length=250,blank=True)
    google_group    = models.EmailField(max_length=100, blank=True, null=True)
    email           = models.EmailField(max_length=100, blank=True, null=True)
    
    
    
    sub_dept = models.ForeignKey(SubDepartment, related_name='parent_department')
    registration_info = models.TextField(max_length=2000,blank=True,null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=50,blank=True)
    event_format = models.TextField(max_length=3000,blank=True,null=True)
    about = models.TextField(max_length=3000,blank=True,null=True)
    faqs = models.ManyToManyField('FAQ',related_name='event_faq',blank=True,null=True)
    FAQs = models.TextField(max_length=5000,blank=True,null=True)
    prizes = models.TextField(max_length=3000,blank=True,null=True)
    is_team = models.BooleanField(default=False,verbose_name='Team Event')
    registration_open = models.BooleanField(default=True)
    registration_close_date = models.DateField(blank=True,null=True)
    contacts = models.TextField(max_length=700,blank=True,null=True)
    options = models.CharField(max_length=5000,blank=True)
    is_active = models.BooleanField(default=True)   
    visible_fields = models.CharField(max_length=10,blank=True,default='11111',verbose_name='Is Active')

    def __unicode__(self):
        return self.name
"""
