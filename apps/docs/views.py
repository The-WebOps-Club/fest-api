# Django
from django.shortcuts import get_object_or_404, render_to_response, redirect, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
# Apps
from misc.utils import *  #Import miscellaneous functions
# Decorators
# Models
# Forms
# View functions
# Misc
# Python

def docs (request):
    return render_to_response('pages/docs.html', context_instance= global_context(request))
