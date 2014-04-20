# Django
from django.shortcuts import get_object_or_404, render_to_response, redirect, HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
# Apps
from misc.utils import *  #Import miscellaneous functions
from apps.docs.utils import Drive, create_flow, get_access_token
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
def docs (request):
    """
        Uhm.
    """
    drive = Drive()
    files = drive.retrieve_all_files()
    local_context = {
        "folder_id" : settings.GOOGLE_DRIVE_ROOT_FOLDER_ID,
    }
    return render_to_response('pages/docs.html', local_context,  context_instance= global_context(request))

def upload_a_file(request):
    """
        Uhm.
    """
    body = {
        'title': 'new function uploaded',
        'description': 'function uploaded A test document',
        'mimeType': 'text/plain'
    }
    fi = '/home/shahidh/works/fest-api/apps/docs/document.txt'
    file = drive().files().insert(body=body, media_body=fi).execute()
    pprint.pprint(file)
    return HttpResponse('done')


@login_required
def picker(request):
    """
        Uhm.
    """
    PARENT_FOLDER_ID = settings.GOOGLE_DRIVE_ROOT_FOLDER_ID
    drive = Drive()
    token = get_access_token()
    return render_to_response('pages/picker.html',locals(), context_instance=global_context(request))

@login_required
def drivebrowse( request ):
    """
        Obtain and send an access token to the client side script.
    """
    PARENT_FOLDER_ID = settings.GOOGLE_DRIVE_ROOT_FOLDER_ID
    api_key = settings.GOOGLE_API_PUBLIC_KEY
    drive = Drive()
    token = get_access_token()
    return render_to_response('pages/drivebrowse.html',locals(), context_instance=global_context(request))

#-------------------------------------------------------------
# One Time actions
@login_required
def get_refresh_token(request):
    '''
        A one time view to get a refresh token from google
    '''
    FLOW = create_flow()
    FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY, request.user)
    authorize_url = FLOW.step1_get_authorize_url()
    return HttpResponseRedirect(authorize_url)

@login_required
def auth_callback(request):
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

@login_required
def initialise_drive(request):
    """
        First time initialisation for the drive folder
        Creates a folder with FEST NAME and share it with
        all the user's email addresses.

        OR MAKE IT PUBLIC?

        Needs to be run on background

        TODO: Write a management script to do this, Add default folders to departments and all
    """
    drive = Drive()
    my_file  = drive.insert_file(settings.FEST_NAME, "Root folder", None, 'application/vnd.google-apps.folder', settings.FEST_NAME, folder=True)
    email_list = [user.email for user in User.objects.all()]
    for email in email_list:
        prems = drive.set_permission(my_file['id'], email, perm_type='user')
    return HttpResponse("<p>Done! Save this as GOOGLE_DRIVE_ROOT_FOLDER_ID in settings.py</p><p>" + str(file['id'])+"</p><p>Close this page</p>")

# a redirect view
def edit_file(request, *args, **kwargs):
    return render_to_response('pages/docframe.html',{'docurl':request.GET['docurl']},RequestContext(request))
