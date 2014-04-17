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
from api import *
from oauth2client.client import flow_from_clientsecrets, Credentials
from oauth2client.django_orm import Storage
from oauth2client import xsrfutil
from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from apiclient import http, errors

###########################################################################################
# These are one time actions, needs to be done per machine/installation. Better move to management command
@login_required
def get_refresh_token(request):
    '''
    Creates a flow object and return url
    '''
    FLOW = create_flow()
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
    FLOW = create_flow()
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
    return HttpResponse("<p>Save this as GOOGLE_API_CREDENTIALS in settings.py</p><p>" + str(credential.to_json())+"</p><p>Close this page</p>")

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
    service = drive()
    file  = insert_file(service, settings.FEST_NAME, "Root folder", None, 'application/vnd.google-apps.folder', settings.FEST_NAME, folder=True)
    new_file = FileInfo.objects.get_or_create(name="ROOT", file_id=file['id'], metadata=json.dumps(file))
    email_list = [user.email for user in User.objects.all()]
    for email in email_list:
        prems = insert_permission(service, file['id'], email, 'user')
    return HttpResponse("<p>Done! Save this as GOOGLE_DRIVE_ROOT_FOLDER_ID in settings.py</p><p>" + str(file['id'])+"</p><p>Close this page</p>")

# End one time actions
##############################################################################################
@login_required
def docs (request):
    # Shall consider moving this to a settings variable, else too much db calls
    try:
        PARENT_FOLDER_ID = settings.GOOGLE_DRIVE_ROOT_FOLDER_ID
        print PARENT_FOLDER_ID
        print "asdasdas"
    except Exception, e:
        raise e
    print PARENT_FOLDER_ID
    files = retrieve_all_files(drive())

    return render_to_response('pages/docs.html',locals(), context_instance= global_context(request))


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



