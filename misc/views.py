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
    print kwargs
    local_context = {
        "current_page" : "err404",
        "messages" : ["hi", "bye"],
    }
    return render_to_response('base/404.html', local_context, context_instance= global_context(request))
    
def err500 (request, *args, **kwargs):
    local_context = {
        "current_page" : "err404",
        "messages" : ["hi", "bye"],
    }
    return render_to_response('base/500.html', local_context, context_instance= global_context(request))

