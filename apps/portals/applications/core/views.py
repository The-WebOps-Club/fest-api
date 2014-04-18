#!/usr/bin/python
# -*- coding: utf-8 -*-

# TODO: Ensure only cores of a department can edit stuff on the department

from django.shortcuts import render_to_response, redirect, HttpResponseRedirect, HttpResponse
from django.template.context import Context, RequestContext
from django.forms.models import modelformset_factory,inlineformset_factory
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.template.defaultfilters import slugify
from django.forms.formsets import formset_factory
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied

from apps.portals.applications.core.models import *
from apps.portals.applications.coord.models import *
from apps.portals.applications.account.models import *
from apps.portals.applications.core.forms import *
#from apps.users.models import Subdept as SubDept

def urlhandler(request):
    return redirect('portal_applications:apps.portals.applications.core.views.core_dashboard',username= request.user )

def handle_permission_exception( in_func ):

    def out_func( request, *args, **kwargs):
        try:
            return in_func( request, *args, **kwargs )
        except PermissionDenied as p:
            return render_to_response('pages/portals/applications/cores/403.html',locals(),RequestContext(request))
    return out_func


def core_test( in_func ):

    def out_func( request, *args, **kwargs ):
        try:
            if not ( request.user.erp_profile.is_core( request ) ):
                raise PermissionDenied('You\'re not a core. These are core waters.... ')
        except:
            raise PermissionDenied('You\'re not a core. These are core waters.... ')
        return in_func( request, *args, **kwargs )

    return out_func


@login_required
@handle_permission_exception
@core_test
def core_dashboard(request,username=None):
    """
    Displays the default dashboard of the core.

    TODO:
    Add is_core decorator
    """
    user = request.user
    subdepts = SubDept.objects.filter(dept=request.user.erp_profile.core_relations.all())
    return render_to_response("pages/portals/applications/cores/core.html",locals(), context_instance=RequestContext(request))

@login_required
@handle_permission_exception
@core_test
def questions_edit(request,username=None,subdept_id=None,q_id=None):
    """
    Working on this.

    This loads up question instance,
    checks if the owner of that question is trying to edit
    it and allows him to do so.
    """
    question=Question.objects.get(id=q_id)
    if (question.subdept.id == int(subdept_id)):
        if request.method!="POST":
            qedit=QuestionForm(instance=question)
            return render_to_response('pages/portals/applications/cores/edit_q.html',locals(), context_instance=RequestContext(request))
        else:
            q=QuestionForm(request.POST,instance=question)
            q.save()
            return redirect('portal_applications:apps.portals.applications.core.views.questions',username=request.user,subdept_id=subdept_id)
    return redirect('portal_applications:apps.portals.applications.core.views.core_dashboard',username=request.user)



@login_required
@handle_permission_exception
@core_test
def questions_delete(request,username=None,subdept_id=None,q_id=None):
    """
    Working on this.

    This loads up question instance,
    checks if the owner of that question is trying to edit
    it and allows him to do so.
    """
    question=Question.objects.get(id=q_id)
    if (question.subdept.id == int(subdept_id)):
        question.delete()
        return redirect('portal_applications:apps.portals.applications.core.views.questions',username=request.user,subdept_id=subdept_id)
    return redirect('portal_applications:apps.portals.applications.core.views.core_dashboard',username=request.user)


@login_required
@handle_permission_exception
@core_test
def questions_all(request,username=None):
    subdepts=SubDept.objects.filter(dept=request.user.erp_profile.core_relations.all())
    if request.method=="POST":
        index=0;
        add_to=request.POST.getlist('subdepartments')
        for x in add_to:
            question=QuestionForm(request.POST)
            if question.is_valid:
                q=question.save(commit=False)
                q.subdept=SubDept.objects.get(id=x)
                q.save()
                index+=1
            else:
                break
    q=QuestionForm()
    return render_to_response("pages/portals/applications/cores/questions_all.html",locals(),context_instance=RequestContext(request))

@login_required
@handle_permission_exception
@core_test
def questions(request,username=None,subdept_id=None):
    """
    Add multiple questions to the application
    questionairre of a particualar SubDept.

    TODO:
    Fucntionality of adding common questions
    to all subdepts under a Dept.
    """
    questions = Question.objects.filter(subdept__pk=subdept_id)
    QuestionFormset = modelformset_factory(Question, form=QuestionForm, extra=5)
    if request.method == 'POST':
        index=0
        questionformset=QuestionFormset(request.POST)
        for questionform in questionformset:
            if questionform.is_valid():
                question=questionform.save(commit=False)
                question.subdept=SubDept.objects.get(pk=subdept_id)
                question.save()
                index+=1
    questionformset = QuestionFormset(queryset=Question.objects.none())
    return render_to_response("pages/portals/applications/cores/questions.html", locals(), context_instance=RequestContext(request))

@login_required
@handle_permission_exception
@core_test
def subdepartments(request,username=None):
    """
    Add Subdepts to a Dept
    """
    #SubdeptFormset = modelformset_factory(SubDept, form=SubDeptForm, extra=3)
    subdept = None
    if request.method == 'POST':
        subdeptform=SubDeptForm( data=request.POST, current_user=request.user )
        if subdeptform.is_valid():
            subdept=subdeptform.save(commit=False)
            subdept.dept_id=subdeptform.cleaned_data['dept_choice']
            subdept.save()
            index=1

    subdeptform = SubDeptForm( current_user = request.user )
    return render_to_response("pages/portals/applications/cores/subdepts.html", locals(), context_instance=RequestContext(request))

"""
@login_required
@core_test
def subdepartments(request,username=None):
    SubdeptFormset = modelformset_factory(SubDept, form=SubDeptForm, extra=3)
    if request.method == 'POST':
        index=0
        subdeptformset=SubdeptFormset(request.POST)
        for subdeptform in subdeptformset:
            if subdeptform.is_valid():
                subdept=subdeptform.save(commit=False)
                subdept.dept=request.user.get_profile().is_core_of
                subdept.save()
                index+=1
    subdeptformset = SubdeptFormset(queryset=SubDept.objects.none())
    return render_to_response("pages/portals/applications/cores/subdepts.html", locals(), context_instance=RequestContext(request))
"""
@login_required
@handle_permission_exception
@core_test
def subdepartments_edit(request,username=None,subdept_id=None):
    """
    Working on this.

    This loads up question instance,
    checks if the owner of that question is trying to edit
    it and allows him to do so.
    """
    subdept=SubDept.objects.get(id=subdept_id)
    if request.method!="POST":
        subedit=SubDeptForm( current_user = request.user, instance=subdept)
        return render_to_response('pages/portals/applications/cores/edit_s.html',locals(), context_instance=RequestContext(request))
    else:
        s=SubDeptForm( current_user = request.user ,  instance=subdept, data = request.POST )
        s.save()
    return redirect('portal_applications:apps.portals.applications.core.views.core_dashboard',username=request.user)

@login_required
@handle_permission_exception
@core_test
def submissions(request,username=None,subdept_id=None):
    """
    Portal to access all submissions
    for a particular subdept.
    """
    if subdept_id:
        AppFormSet = modelformset_factory(Application, form=SelectAppForm)
        subdept = SubDept.objects.get(id = subdept_id)
        applications  = Application.objects.filter(subdept = subdept)
        if request.method=="POST":
            appformset = AppFormSet(request.POST)
            for appform in appformset:
                if appform.is_valid():
                    app = appform.save()
                    if app.rank > 0:
                        app.status = 'accepted'
                    elif app.rank == 0:
                        app.status = 'rejected'
                    else:
                        app.status = 'pending'
                    app.save()
            saved = True
        else:
            appformset = AppFormSet(queryset=Application.objects.filter(subdept=subdept))
        app_details = zip(applications,appformset)
    else:
        return redirect('portal_applications:apps.portals.applications.core.views.core_dashboard',username=request.user)
    return render_to_response("pages/portals/applications/cores/submissions.html",locals(), context_instance=RequestContext(request))


@login_required
@handle_permission_exception
@core_test
def applicants(request,username=None,applicant=None):
    """
    Portal to view all details about an applicant.
    """
    applicant = User.objects.get(username=applicant)
    applicant_profile = applicant.application_profile.all()[0]
    applications = Application.objects.filter(user=applicant).exclude(preference = -1)
    return render_to_response("pages/portals/applications/cores/applicant.html",locals(), context_instance=RequestContext(request))

@login_required
@handle_permission_exception
@core_test
def applications(request,username=None,app_id=None):
    """
    Portal to view the details of a particular application
    """
    app = Application.objects.get(id=app_id)
    if app.subdept.dept not in request.user.erp_profile.core_relations.all():
        return redirect('portal_applications:apps.portals.applications.core.views.applicants', username=request.user, applicant = app.user)

    answers   = app.answers.all()
    questions = [ans.question for ans in answers]
    comments = Comments.objects.filter(answer__in=answers)
    CommentsFormSet = modelformset_factory(Comments, form=CommentsForm, extra=0)
    if request.method == "POST":
        commentsformset = CommentsFormSet(request.POST)
        appcommentsform = AppCommentsForm(request.POST,instance=AppComments.objects.get(app=app))
        if appcommentsform.is_valid():
            appcommentsform.save()
        for commentsform in commentsformset:
            if commentsform.is_valid():
                data = commentsform.cleaned_data
                commentsform.save()
        saved = True
    else:
        appcommentsform = AppCommentsForm(instance=AppComments.objects.get(app=app))
        commentsformset = CommentsFormSet(queryset=comments)
    qna = zip(questions,answers,commentsformset)
    return render_to_response("pages/portals/applications/cores/application.html",locals(), context_instance=RequestContext(request))

@login_required
@handle_permission_exception
@core_test
def cgpa_filter(request,username=None,subdept_id=None,default=7.0):
    subdept=SubDept.objects.get(id=subdept_id)
    apps=Application.objects.filter(subdept__id=subdept_id)
    for app in apps:
        if app.user.application_profile.all()[0].cgpa<default:
            app.status='rejected'
            app.rank=-1
            app.save()
    return redirect('portal_applications:apps.portals.applications.core.views.submissions',username=request.user,subdept_id=subdept_id)

@login_required
@handle_permission_exception
@core_test
def add_instructions(request, username = None,subdept_id = None):
    subdept=SubDept.objects.get(id=subdept_id)
    try:
        instr = Instructions.objects.get(sub_dept = subdept)
        form = InstructionsForm(instance = instr)
        if request.method == 'POST':
            form = InstructionsForm(request.POST,instance = instr)
            if form.is_valid():
                f = form.save() 
                return redirect('portal_applications:apps.portals.applications.core.views.core_dashboard',username=request.user)  
    except:
        form = InstructionsForm()
        if request.method == 'POST':
            form = InstructionsForm(request.POST)
            if form.is_valid():
                f = form.save(commit = False) 
                f.sub_dept = subdept 
                f.save()
                return redirect('portal_applications:apps.portals.applications.core.views.core_dashboard',username=request.user)  
    return render_to_response("pages/portals/applications/cores/instructions.html",locals(), context_instance=RequestContext(request))    

@login_required
@handle_permission_exception
@core_test
def instructions_all(request,username=None):
    subdepts=SubDept.objects.filter(dept=request.user.erp_profile.core_relations.all())
    if request.method=="POST":
        index=0;
        add_to=request.POST.getlist('subdepartments')
        for x in add_to:
            instruction=InstructionsForm(request.POST)
            if instruction.is_valid:
                i = None
                # try to get an instructions object. if it DoesNotExist, create a new one.
                try:
                    i = Instructions.objects.get( sub_dept_id = x )
                    #import pdb;pdb.set_trace()
                    i.instructions += instruction.data['instructions'] + "\n"
                except:
                    i = instruction.save(commit=False)
                    i.sub_dept=SubDept.objects.get(id=x)
                
                i.save()
                index+=1
            else:
                break
    i=InstructionsForm()
    return render_to_response("pages/portals/applications/cores/instructions_all.html",locals(), context_instance=RequestContext(request))
