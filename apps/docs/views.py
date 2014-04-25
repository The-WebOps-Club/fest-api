# Django
from django.shortcuts import get_object_or_404, render_to_response, redirect, HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
# Apps
from misc.utils import *  #Import miscellaneous functions
from apps.docs.utils import Drive, Github
# Decorators
# Models
# from apps.docs.models import CredentialsModel, FileInfo
from django.contrib.auth.models import User
# Forms
# View functions
# Misc
from annoying.functions import get_object_or_None
# Python
import json
import httplib2
import pprint
import os
# For google Drive
from oauth2client.client import flow_from_clientsecrets, Credentials
from oauth2client.django_orm import Storage
from oauth2client import xsrfutil
from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from apiclient import http, errors


#-------------------------------------------------------------
# Gen views
@login_required
def docs( request ):
    """
        Obtain and send an access token to the client side script.
    """
    drive = Drive()
    token = Drive.get_access_token()
    user_list = User.objects.all()
    local_context = {
        "token" : token,
        "current_page" : "docs",
    }
    return render_to_response('pages/browse_docs.html', locals(), context_instance=global_context(request))

@login_required
def picker(request):
    """
        Uhm.
    """
    PARENT_FOLDER_ID = settings.GOOGLE_DRIVE_ROOT_FOLDER_ID
    drive = Drive()
    token = Drive.get_access_token()
    print Drive
    return render_to_response('pages/picker.html',locals(), context_instance=global_context(request))

@login_required
def edit_file(request, *args, **kwargs):
    local_context = {
        'docurl' : request.GET['docurl'],
    }
    return render_to_response('pages/view_doc.html', local_context, RequestContext(request))

#-------------------------------------------------------------
# One Time actions
    # GITHUB
@login_required
def github_refresh_token(request):
    '''
        A one time view to get a refresh token from google
    '''
    FLOW = create_flow()
    FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY, request.user)
    authorize_url = FLOW.step1_get_authorize_url()
    return HttpResponseRedirect(authorize_url)

@login_required
def github_auth_callback(request):
    '''
        Auth Callback to save the given google_api_credentials json into a file for later use
    '''
    FLOW = create_flow()
    if not xsrfutil.validate_token(settings.SECRET_KEY, request.REQUEST['state'], request.user):
        return  HttpResponseBadRequest()
    credential = FLOW.step2_exchange(request.REQUEST)
    # Store to file
    docs_client_json = str(credential.to_json())
    file_path = settings.GOOGLE_API_CREDENTIALS_FILE_PATH
    with open(file_path, 'w') as f:
        f.write(docs_client_json)

    return HttpResponse("Restart your server for google drive to work.")

    # Google
@login_required
def google_refresh_token(request):
    '''
        A one time view to get a refresh token from google
    '''
    FLOW = Drive.create_flow()
    FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY, request.user)
    authorize_url = FLOW.step1_get_authorize_url()
    return HttpResponseRedirect(authorize_url)

@login_required
def google_auth_callback(request):
    '''
        Auth Callback to save the given google_api_credentials json into a file for later use
    '''
    FLOW = Drive.create_flow()
    if not xsrfutil.validate_token(settings.SECRET_KEY, request.REQUEST['state'], request.user):
        return  HttpResponseBadRequest()
    credential = FLOW.step2_exchange(request.REQUEST)
    # Store to file
    docs_client_json = str(credential.to_json())
    file_path = settings.GOOGLE_API_CREDENTIALS_FILE_PATH
    with open(file_path, 'w') as f:
        f.write(docs_client_json)

    return HttpResponse("Restart your server for google drive to work.")
