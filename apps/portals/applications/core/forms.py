#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from django import forms
from django.forms import ModelForm, Form
from apps.portals.applications.core.models import *
from apps.portals.applications.coord.models import *
from apps.portals.applications.account.models import *
#from apps.users.models import Subdept as SubDept

class QuestionForm(ModelForm):
    """
    Form that allows cores to add
    questions to a specific subdept.
    """
    class Meta:
        model=Question
        exclude=('subdept',)

    def __init__(self, *arg, **kwarg):
        super(QuestionForm, self).__init__(*arg, **kwarg)
        self.empty_permitted = False

class AllQuestionForm(ModelForm):
    choices = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)
    class Meta:
        model=Question
        exclude=('subdept',)

    def __init__(self,*arg,**kwarg):
        super(AllQuestionForm, self).__init__(*arg,**kwarg)
        self.empty_permitted = False

class SubDeptForm(ModelForm):
    """
    Form that allows adding subdepts.
    """
    dept_choice = forms.ChoiceField()
    class Meta:
        model=SubDept
        exclude=('dept',)

    def __init__(self, current_user=None, *args, **kwargs):
        #import pdb;pdb.set_trace()
        super(SubDeptForm, self).__init__(*args, **kwargs)
        
        self.fields['dept_choice'].choices = [(x.id,x.name) for x in current_user.erp_profile.core_relations.all()]
        self.empty_permitted = False

class SelectAppForm(ModelForm):
    """
    Form that allows selecting and giving ranks to the submissions
    """
    class Meta:
        model = Application
        fields = ('rank','status',)
        widgets = {'status':forms.HiddenInput(),}

class CommentsForm(forms.ModelForm):
    """
    Form for the core to add comments about a specific answer
    """
    class Meta:
        model   = Comments
        fields  = ('answer','comment',)
        widgets = {'answer': forms.HiddenInput(),}

class AppCommentsForm(forms.ModelForm):
    """
    Model Form for the core to add general comment/feedback about the
    application to the aspiring coordinator.
    """
    class Meta:
        model   = AppComments
        fields  = ('app','comment',)
        widgets = {'app': forms.HiddenInput(),}

class InstructionsForm(forms.ModelForm):
    """
    Model Form for the core to add instructions to a sub department
    """
    class Meta:
        model   = Instructions
        exclude = ('sub_dept',)

