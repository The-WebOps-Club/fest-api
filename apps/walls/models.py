"""
    Handles all models related to walls :
        - Wall : The general model declaring everything inside a class
        - Post : The basic fucntioning unit of a Wall - Posts. 

"""
# Django
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Apps
# Decorators
# Models
# Forms
# View functions
# Misc
from misc.utils import *
# Python

# Model for Department forum
class Wall(models.Model):
    '''
        Defines a Wall - a wall can be of a person, department or subdepartment
        It is linked using a OneToOne field on the side of the Person, Department or SubDepartment
        
        @todo : Add analytics to be able to see when each person saw the wall last
    '''
    
    # Basic information
    name            = models.CharField(max_length=60, unique=True)
    
    # Relations with other models
    owners          = models.ManyToManyField(User, null=True, blank=True, related_name='walls') # People who get notifications about this wall
    
    # Analytics
    
    @property
    def parent(self):
        temp = None
        try : temp = self.person()
        except AttributeError as ae2: 
            try : temp = self.dept()
            except AttributeError as ae2: 
                try : temp = self.subdept()
                except AttributeError as ae3: 
                    temp = None
            
        return temp
    
    def __unicode__(self):
        return self.name
    
class Post(models.Model):
    '''
        Defines the Post class. The model which has some kind of data about a message.
        
        @todo : Add options to upload a file to any message
    '''
    # Basic data
    description = models.TextField(blank=True, default='') # The matter of post
    
    # Relations with various other models
    wall            = models.ForeignKey(Wall, related_name='posts', blank = True, null = True)
    child           = models.OneToOneField('self', related_name='parent', blank = True, null = True)
    by              = models.ForeignKey(User, related_name='posts_created')
    
    # Analytics
    time_created    = models.DateTimeField(auto_now_add=True)
    time_updated    = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title
    
    
    def __unicode__(self):
        LIMIT = 50
        tail = len(self.description) > LIMIT and '...' or ''
        return self.description[:LIMIT] + tail

    class Meta:
        ordering = ['time_created']
        get_latest_by = 'time_created'

    def __unicode__(self):
        return self.description


