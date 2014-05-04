# Django
from django.shortcuts import render_to_response, redirect, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.conf import settings
# Apps
from misc.utils import *  #Import miscellaneous functions
# Decorators
# Models
from django.contrib.auth.models import User
# Forms
# View functions
# Misc
from django.templatetags.static import static
# Python
import os
import random

def err404 (request, *args, **kwargs):
    num = random.randint(1, 9)
    local_context = {
        "SITE_URL"  : settings.SITE_URL,
        "num" : num,
    }
    return render_to_response('errors/404.html', local_context, context_instance=global_context(request, token_info=False))
    
def err500 (request, *args, **kwargs):
    num = random.randint(1, 3)
    local_context = {
        "SITE_URL"  : settings.SITE_URL,
        "num" : num,
    }
    return render_to_response('errors/500.html', local_context, context_instance=global_context(request, token_info=False))

def setup(request, *args, **kwargs):
    local_context = {
    }
    return render_to_response('pages/setup.html', local_context, context_instance= global_context(request, token_info=False, user_info = False))
