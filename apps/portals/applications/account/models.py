#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from apps.portals.applications.core.models import *


HOSTEL_CHOICES = (
    ('Alakananda','Alakananda'),
    ('Brahmaputra','Brahmaputra'),
    ('Cauvery','Cauvery'),
    ('Ganga','Ganga'),
    ('Godavari','Godavari'),
    ('Jamuna','Jamuna'),
    ('Krishna','Krishna'),
    ('Mahanadhi','Mahanadhi'),
    ('Mandakini','Mandakini'),
    ('Narmada','Narmada'),
    ('Pamba','Pamba'),
    ('Saraswati','Saraswati'),
    ('Sarayu','Sarayu'),
    ('Sharavati','Sharavati'),
    ('Sindhu','Sindhu'),
    ('Tamiraparani','Tamiraparani'),
    ('Tapti','Tapti'),
)

DEPT_CHOICES = (
    ('Design','Design'),
    ('Events','Events'),
    ('Evolve','Evolve'),
    ('Facilities','Facilities'),
    ('Finance','Finance'),
    ('QMS','QMS'),
    ('Shows','Shows'),
    ('Sponsorship and PR','Sponsorship and PR'),
    ('Student Relations','Student Relations'),
    ('Webops','Webops'),    
)
class UserProfile(models.Model):
    """
        Stores the Profile details of the Users (both Coordinators and Cores).
    """
    user            = models.ForeignKey(User, unique=True, related_name='application_profile' )
    nick            = models.CharField(max_length = 20, blank = True)
    room_no         = models.CharField(max_length = 5, blank = False, null = False)
    hostel          = models.CharField(max_length = 40, choices = HOSTEL_CHOICES, blank = False, null = False)
    ph_no           = models.CharField(max_length = 15, unique = True, blank = False, null = False,help_text = "Do NOT enter 0 or +91 before your 10 digit mobile number")
    city            = models.CharField(max_length = 15, blank = False, null = False, help_text = "Which city are you from?")
    summer_location = models.CharField(max_length = 15, blank = False, null = False, help_text = "Where will you be during summer vacation?")
    is_core_of      = models.CharField(max_length = 40, choices = DEPT_CHOICES, null = True, blank = True)
    cgpa            = models.FloatField()

    def CoreSubDepts(self):
        if self.is_core_of is '':
            return False
        else:
          pass
          #return SubDept.objects.filter(dept=is_core_of)
    
    def __unicode__(self):
        return str(self.user.username)

class Announcement(models.Model):
    """
      Stores announcements that will be displayed in the login screen.
      This model objects will be handled from the django admin site.
    """
    message     = models.TextField()
    timestamp   = models.TimeField(auto_now = True, editable = False)
    
    def __unicode__(self):
        return self.    message

