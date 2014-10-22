
"""
    Handles all models related to events :
        - Event : Information about an event in Fest
        - Tab : Information about an event tab in Fest
        
        This models.py has been combined with apps/portals/models.py

"""
# Django
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
# Apps
import select2.fields
# Decorators
# Models
from apps.walls.models import Wall, Post
from apps.users.models import User,UserProfile,Team,ERPProfile
# Forms
# View functions
# Misc
from misc.utils import *
# Python
from configs.settings import FEST_NAME
import select2.models
import select2.forms


if FEST_NAME=='Saarang':
	EVENT_CATEGORIES = (
		('Word Games', 'Word Games'),
		('Classical Arts', 'Classical Arts'),
		('LecDems', 'LecDems'),
		('Music', 'Music'),
		('Thespian', 'Thespian'),
		('Writing', 'Writing'),
		('Speaking', 'Speaking'),
		('Choreo', 'Choreo'),
		('Design & Media', 'Design & Media'),
		('Informals', 'Informals'),
		('Quizzing', 'Quizzing'),
		('Fine Arts', 'Fine Arts'),
	)
else:
	EVENT_CATEGORIES = (
		('Aerofest', 'Aerofest'),
		('Coding', 'Coding'),
		('Design and build', 'Design and build'),
		('Involve', 'Involve'),
		('Quizzes', 'Quizzes'),
		('Online', 'Online'),
		('Department Flagship Event', 'Department Flagship Event'),
		('Spotlight', 'Spotlight'),
		('Workshops', 'Workshops'),
		('Exhibitions', 'Exhibitions and Shows'),
		('Miscellaneous', 'Miscellaneous'),
		('Sampark', 'Sampark'),
		('B- Events','B- Events'),
		('Associated Events','Associated Events'),
	)

EVENT_TYPE = (
    ('Audience', 'Audience'),
    ('Participant', 'Participant'),
    ('None','None'),
)
    
class Event(models.Model):
    """
        An Event model which defines every event happening in the fest.
        #question : Should FAQ be a different model ? Why was it kept like this in saarang ?
    """
    
    # Basic information
    name                = models.CharField(max_length=50, unique=True)
    short_description   = models.CharField(max_length=250, blank=True)
    event_type          = models.CharField(max_length=100, choices=EVENT_TYPE, blank=True, null=True)
    category            = models.CharField(max_length=100, choices=EVENT_CATEGORIES)
    
    # Event - Team specific information
    has_tdp             = models.BooleanField(default=False)
    team_size_min       = models.IntegerField(default=1, blank=True, null=True) # Team event or not can be got using these fields
    team_size_max       = models.IntegerField(default=1, blank=True, null=True)
    
    # Event registration information
    registration_starts = models.DateTimeField(blank=True, null=True) # Using the two dates it can be found if registration is on or not
    registration_ends   = models.DateTimeField(blank=True, null=True)
    
    # Email ids specific to the Event : google_group and the corresponding shaatsra_email_id
    google_group        = models.EmailField(max_length=100, blank=True, null=True)
    email               = models.EmailField(max_length=100, blank=True, null=True)

	# List of registered participants
    users_registered = models.ManyToManyField(User, blank=True, null=True,related_name='events_registered')
    teams_registered = models.ManyToManyField(Team, blank=True, null=True,related_name='events_registered')
    #added by Akshay/Arun
    coords = models.ManyToManyField(ERPProfile, null=True, blank=True, related_name='coord_events')
    long_description=models.TextField(blank = True, null=True)
    google_form=models.URLField(blank=True, null=True)
    event_image=models.ImageField(upload_to="events",blank=True, null=True)
    # Extra mainsite information
    is_visible = models.BooleanField(default=True) # On the mainsite
    
    # Some properties to make some conditions easier
    @property
    def is_team_event(self):        
        return self.team_size_max > 1
    @property
    def is_registration_on(self):   
        return timezone.now() > self.registrarion_starts and timezone.now() < self.registrarion_ends
        
    # Other methods
    def __unicode__(self):
        return self.name

class Tab(models.Model):
    """
        A model containing data for a tab that is displayed for the events on the mainsite
    """
    # Relation to various other models
    event           = models.OneToOneField(Event, blank=True, null=True)
    
    # Baisc information
    head            = models.CharField(max_length=100)
    content         = models.TextField(blank = True)
    
    # Extra information about how the tab is shown on mainsite
    order           = models.IntegerField(default=0, blank=False) # Tells which tab should come first in the list
    is_visible      = models.BooleanField(default=True) # On the mainsite
    
    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['order']



#New


class EventTab(models.Model):
    """
       Each event will have several tabs. This is one of them
    """
    # Relation to various other models
    event           = models.ForeignKey(Event)
    
    # Baisc information
    name            = models.CharField(max_length=100)
    content         = models.TextField(blank = True)
    

    def __unicode__(self):
        return self.name

class EventRegistration(models.Model):
    """
        Each participant will have several fields 
    """
    event            = models.ForeignKey(Event, related_name='event_registered')
    users_registered = models.ForeignKey(User, related_name='user_eventregis')
    timestamp        = models.DateTimeField(auto_now_add=True)
    teams_registered = models.ForeignKey(Team, blank=True, null=True,related_name='user_team')
