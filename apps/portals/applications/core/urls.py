#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$','apps.portals.applications.core.views.urlhandler'),
    url(r'^(?P<username>\w+)/questions/(?P<subdept_id>\w+)/$','apps.portals.applications.core.views.questions',name='core_questions'),
    url(r'^(?P<username>\w+)/questions/(?P<subdept_id>\w+)/(?P<q_id>\w+)/$','apps.portals.applications.core.views.questions_edit',name='core_questions_edit'),
    url(r'^(?P<username>\w+)/delete/(?P<subdept_id>\w+)/(?P<q_id>\w+)/$','apps.portals.applications.core.views.questions_delete',name='core_questions_delete'),
    url(r'^(?P<username>\w+)/questions-all/','apps.portals.applications.core.views.questions_all',name='core_questions_all'),
    url(r'^(?P<username>\w+)/subdepartments/(?P<subdept_id>\w+)/$','apps.portals.applications.core.views.subdepartments_edit',name='core_subdepartments_edit'),
    url(r'^(?P<username>\w+)/subdepartments/$','apps.portals.applications.core.views.subdepartments',name='core_subdepartments'),
    url(r'^(?P<username>\w+)/dashboard/$', 'apps.portals.applications.core.views.core_dashboard', name='core_home'),
    url(r'^(?P<username>\w+)/submissions/(?P<subdept_id>\w+)/','apps.portals.applications.core.views.submissions',name='core_submissions'),
    url(r'^(?P<username>\w+)/instructions/(?P<subdept_id>\w+)/','apps.portals.applications.core.views.add_instructions',name='add_instructions'),
    url(r'^(?P<username>\w+)/instructions-all/','apps.portals.applications.core.views.instructions_all',name='core_instructions_all'),
    url(r'^(?P<username>\w+)/cgpafilter/(?P<subdept_id>\w+)/$','apps.portals.applications.core.views.cgpa_filter',name='core_cgpa_filter'),
    url(r'^(?P<username>\w+)/applicants/(?P<applicant>\w+)/','apps.portals.applications.core.views.applicants',name='core_applicants'),
    url(r'^(?P<username>\w+)/applications/(?P<app_id>\w+)/','apps.portals.applications.core.views.applications',name='core_applications'),
)

