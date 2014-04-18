#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from apps.portals.applications.account.views import *
from django.contrib.auth.views import password_change
from django.conf import settings

urlpatterns = patterns('',
    url(r'^password_change/$', password_change,{'post_change_redirect':settings.SITE_URL}),
    url(r'^login/$', 'apps.portals.applications.account.views.login', name='login'),
    url(r'^register/$', 'apps.portals.applications.account.views.register', name='home'),
    url(r'^logout/$', 'apps.portals.applications.account.views.logout', name='logout'),
    url(r'^editprofile/$', 'apps.portals.applications.account.views.editprofile', name='editprofile'),
)

