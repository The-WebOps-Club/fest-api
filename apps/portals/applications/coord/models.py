#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from apps.portals.applications.account.models import DEPT_CHOICES
from apps.portals.applications.core.models import Question, SubDept

STATUS_CHOICES=(
        ('accepted','Accepted'),
        ('pending','Pending'),
        ('rejected','Rejected'),
        )

class Answer(models.Model):
    """
    Stores a textfield answer to each question.
    """
    question = models.ForeignKey(Question, null = True)
    answer   = models.TextField(blank = True)

    def __unicode__(self):
        return u'%s' % (self.answer)
    
    def get_short_content(self):
        return u'%s...' % (self.answer[:10])
        

class Credential(models.Model):
    """
    Stores credentials of the user.

    TODO:
    Add a key to user if you want credential
    details specifically.
    """
    content = models.TextField(blank=True)

    def __unicode__(self):
        return u'%s'% (self.content)
        
    def get_short_content(self):
        return u'%s...' % (self.content[:10])
        

class Reference(models.Model):
    """
    Stores references given by the user.

    TODO:
    Add a key if you want user-specific
    references
    """
    content = models.TextField(blank=True)

    def __unicode__(self):
        return u'%s' % (self.content)
        
    def get_short_content(self):
        return u'%s...' % (self.content[:10])
        

class Application(models.Model):
    """
    Stores each application made by
    aspiring coords with keys to
    credentials and references.
    """
    user        = models.ForeignKey(User)
    subdept     = models.ForeignKey(SubDept)
    answers     = models.ManyToManyField(Answer)
    preference  = models.IntegerField(default=1)
    credentials = models.ForeignKey(Credential)
    references  = models.ForeignKey(Reference)
    lockstatus  = models.BooleanField(default=False)
    timestamp   = models.DateTimeField(auto_now=True, editable=False)
    rank    = models.IntegerField(default=-1) # This field determines if the core has selected the application and the priority assigned
    status = models.CharField(max_length='10',choices=STATUS_CHOICES,default='pending')
    
    def pass_cgpa(self):
        return True
