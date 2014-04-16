# Django
from django.conf import settings
from django.shortcuts import render_to_response, redirect, HttpResponseRedirect
from django.core.urlresolvers import resolve, reverse
# Apps
# Decorators
# Models
from django.contrib.auth.models import User
# Forms
# View functions
# Misc
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

