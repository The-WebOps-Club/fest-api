# Django
from django.shortcuts import get_object_or_404, render_to_response, redirect, HttpResponseRedirect, HttpResponse
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

from authorize import get_credentials, get_authorization_url
from test import get_authorisation_code

def docs (request):
    authorize_url = get_authorization_url('festapi14@gmail.com', 'urls')
    return render_to_response('pages/docs.html',locals(), context_instance= global_context(request))

def oauth2callback (request):
    get = request.GET.copy()
    code = get['code']
    print code
    cred = get_credentials(code, 'response_from_callback')
    print cred.to_json()
    return HttpResponse(code)
