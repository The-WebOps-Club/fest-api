# Django
from django.conf import settings
from django.template.context import Context, RequestContext
from django.shortcuts import render_to_response, redirect, HttpResponseRedirect
from django.core.urlresolvers import resolve, reverse
from django.core.files.base import ContentFile
# Apps
from apps.users.utils import send_email_validation_mail, send_registration_mail
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
import datetime
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
        
        profile = user.profile
        profile.fb_id
        #profile.save()

def check_existing_user(strategy, details, response, uid, user=None, *args, **kwargs):
    if user:
        return {'is_new': False}

    try:
        if(strategy.session_get('type') == 'participant'):
            return;
    except:
        pass;
    return user
#    return redirect('apps.users.views.first_login_required')

# Send Confirmation email

def send_welcome_email(user, details, is_new=False, new_association=False, **kwargs):
    print "is new ========================== ", is_new
    print "new association ================= ", new_association
    print user.last_login
    if is_new or user.last_login < datetime.datetime(2015, 12, 10, 0, 0):
        send_registration_mail(user)
