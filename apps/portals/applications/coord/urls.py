#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from apps.portals.applications.account.views import *

urlpatterns = patterns('',
    url(r'^application/(?P<sub_dept_id>\d+)', 'apps.portals.applications.coord.views.application', name='application'),
    url(r'^delete/(?P<sub_dept_id>\d+)', 'apps.portals.applications.coord.views.delete', name='delete'),
    url(r'^', 'apps.portals.applications.coord.views.coord_home', name='coord_home'),
)

