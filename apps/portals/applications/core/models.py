#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
#from apps.portals.applications.account.models import DEPT_CHOICES
#from apps.portals.applications.core.models import Subdept as SubDept
from apps.users.models import Dept

class SubDeptManager(models.Manager):
    def all(self):
                return self.filter(close_apps=False)



"""class SubDept(models.Model):
#    
#      Each department under Shaastra has sub-departments.
#      Example: Design is a Department whereas Graphic Design, Photography etc are sub-departments

#    
    dept        = models.CharField(max_length = 40, choices = DEPT_CHOICES)
    name        = models.CharField(max_length = 1000)
    impose_cgpa = models.BooleanField(default = True, help_text="This does not work, don't bother")
    close_apps  = models.BooleanField(default = False, help_text="Decides whether coord aspirants can apply for the Subdept or not")

    objects = SubDeptManager()

    def __unicode__(self):
        return "%s | %s " %(self.dept,self.name)

    def get_short_name(self):
        return self.name
"""

# expermental SubDept
class SubDept(models.Model):
    """ 
        Temprary model for experimental sub depts. A backend function will soon change the Temporary model to a fully-fledged model.
        A model having data about specific SubDepartments @ the fest 
        Every subdept is linked to an event 
    """
    # Relations with other models
    dept            = models.ForeignKey(Dept, related_name='experimental_subdepts')
    # wall            = models.OneToOneField(Wall, related_name='subdept')
    # event           = models.ForeignKey(Event, null=True, blank=True)
    
    # Basic information
    name            = models.CharField(max_length=30, unique=True)
    description     = models.TextField(max_length=500, null=True, blank=True)

    def __unicode__(self):
        return self.name

    def cores(self):
        return [i.user for i in self.dept.core_set.all()]
    def supercoords(self):
        return [i.user for i in self.dept.supercoord_set.all()]
    def coords(self):
        return [i.user for i in self.coord_set.all()]
    def related_users(self):
        ret = set()
        ret.update( self.coords(), self.supercoords(), self.cores() )
        return list(ret)

class Question(models.Model):
    """
      Each Sub-department has specific questionnaire. This model is for storing the questions and
      to which sub-department they are meant for.

    """
    subdept  = models.ForeignKey(SubDept)
    question = models.TextField()

    def __unicode__(self):
        return str(self.question)
        
    def get_short_content(self):
        return "%s..." % str(self.question[:10])

from apps.portals.applications.coord.models import Answer, Application

class Comments(models.Model):
    """
    Stores comments written by Cores about an answer in an application.
    This helps the core during the interview.
    """
    answer  = models.ForeignKey(Answer)
    comment = models.TextField(blank=True)
    
    def __unicode__(self):
        return str(self.comment)

class AppComments(models.Model):
    """
    Stores comments written by Cores about an application in general.
    This serves as a useful feedback to the aspiring coordinator who can view this at the end of selection procedure.
    """
    app     = models.ForeignKey(Application,unique=True)
    comment = models.TextField(blank=True)
    
    def __unicode__(self):
        return str(self.comment)

class Instructions(models.Model):
    """
    Stores Sub - Department specific instructions
    """
    sub_dept        = models.ForeignKey(SubDept,unique=True, null = True)
    instructions    = models.TextField(blank = True)
    
    def __unicode__(self):
        return str(self.instructions)

