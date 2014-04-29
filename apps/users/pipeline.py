# Django
from django.conf import settings
from django.template.context import Context, RequestContext
from django.shortcuts import render_to_response, redirect, HttpResponseRedirect
from django.core.urlresolvers import resolve, reverse
from django.core.files.base import ContentFile
# Apps
# Decorators
# Models
from django.contrib.auth.models import User
# Forms
# View functions
# Misc
from requests import request, HTTPError
from misc.utils import *
from social.pipeline.partial import partial
# Python

@partial
def require_email(strategy, details, user=None, is_new=False, *args, **kwargs):
    if user and user.email:
        return
    elif is_new and not details.get('email'):
        if strategy.session_get('saved_email'):
            details['email'] = strategy.session_pop('saved_email')
        else:
            return redirect('require_email')

@partial
def save_profile_picture(strategy, user, response, details, is_new=False, *args, **kwargs):
    if strategy.backend.name == 'facebook':
        url = 'http://graph.facebook.com/{0}/picture'.format(response['id'])
        print url

        profile = user.profile
        profile.fb_id
        #profile.save()

def check_existing_user(strategy, details, response, uid, user=None, *args, **kwargs):
    if user:
        return {'is_new': False}
    return redirect('apps.users.views.first_login_required')

