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

def err404 (request, *args, **kwargs):
    err404page = True
    return render_to_response('pages/404.html', locals(), context_instance= global_context(request))
    
def err500 (request, *args, **kwargs):
    err500page = True
    return render_to_response('pages/500.html', locals(), context_instance= global_context(request))

