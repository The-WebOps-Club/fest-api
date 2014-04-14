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
# from models import StoredCredential
# import logging
# # Forms
# # View functions
# # Misc
# # Python
# import json
# from authorize import get_credentials, get_authorization_url
# # from test import get_authorisation_code
from oauth2client.client import flow_from_clientsecrets, Credentials
from oauth2client.django_orm import Storage
from oauth2client import xsrfutil
from django.contrib.auth.models import User
from models import CredentialsModel
from annoying.functions import get_object_or_None
import json
import httplib2
from apiclient.discovery import build
from apiclient.http import MediaFileUpload
import pprint

FLOW = flow_from_clientsecrets(
    settings.GOOGLE_API_CLIENT_SECRETS, 
    ' '.join(settings.GOOGLE_API_SCOPES),
    redirect_uri=settings.GOOGLE_API_REDIRECT_URI)
FLOW.params['access_type'] = 'offline'
FLOW.params['approval_prompt'] = 'force'
@login_required
def get_refresh_token(request):
    if not request.user == User.objects.get(email=settings.GOOGLE_API_USER_EMAIL):
        return HttpResponse("You are not authorised to access the drive API")
    # storage = Storage(CredentialsModel, 'id', request.user, 'credential')
    # credential = storage.get()
    storage = get_object_or_None(CredentialsModel, id=request.user)
    try:
        credential = Credentials.new_from_json(json.loads(storage.credential))
    except Exception,e:
        credential = None
    if credential is None or credential.invalid == True:
        FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY, request.user)
    authorize_url = FLOW.step1_get_authorize_url()
    return HttpResponseRedirect(authorize_url)

@login_required
def auth_callback(request):
    if not xsrfutil.validate_token(settings.SECRET_KEY, request.REQUEST['state'], request.user):
        return  HttpResponseBadRequest()
    credential = FLOW.step2_exchange(request.REQUEST)
    # storage = Storage(CredentialsModel, 'id', request.user, 'credential')
    # storage.put(credential)
    storage = CredentialsModel.objects.get_or_create(id = request.user)
    storage = storage[0]
    storage.credential = credential.to_json()
    storage.refresh_token = credential.refresh_token
    storage.save()
    return redirect('docs')

@login_required
def docs (request):
    PARENT_FOLDER_ID = '0B75xGGtqUve5eHhzcWdCR2VHcnc'
    return render_to_response('pages/docs.html',locals(), context_instance= global_context(request))


def drive():
    """
        Args: None
        Returns: Authenticated drive service object

        Currently assuming there will be only one Credential
        saved by the user having settings.GOOGLE_API_USER_EMAIL as email
    """
    try:
        storage = CredentialsModel.objects.all()[0]
    except CredentialsModel.DoesNotExist:
        return redirect('get_refresh_token')
    credential = Credentials.new_from_json(storage.credential)
    http = httplib2.Http()
    http = credential.authorize(http)
    return build('drive', 'v2', http=http)


#Sample function to upload a file
def upload_a_file(request):
    body = {
        'title': 'new function uploaded',
        'description': 'function uploaded A test document',
        'mimeType': 'text/plain'
    }
    fi = '/home/shahidh/works/fest-api/apps/docs/document.txt'
    file = drive().files().insert(body=body, media_body=fi).execute()
    pprint.pprint(file)
    return HttpResponse('done')

def initialise_drive():
    """
        First time initialisation for the drive folder
        Creates a folder with FEST NAME and share it with
        all the user's email addresses.

        OR MAKE IT PUBLIC?
    """
    return
