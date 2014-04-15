# From Django
from django.shortcuts import get_object_or_404, render_to_response, redirect, HttpResponseRedirect, HttpResponse
from django.conf import settings
# From Google API
from apiclient import errors, http
from apiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets, Credentials
from apiclient.discovery import build
# Apps
from misc.utils import *  #Import miscellaneous functions
# Decorators
# Models
from models import CredentialsModel, FileInfo
# Forms
# View functions
# Misc
# Python
import httplib2, json
# ...

def create_flow():
  pass

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

def insert_file(service, title, description, parent_id, mime_type, filename, folder=False):
  """Insert new file.

  Args:
    service: Drive API service instance.
    title: Title of the file to insert, including the extension.
    description: Description of the file to insert.
    parent_id: Parent folder's ID.
    mime_type: MIME type of the file to insert.
    filename: Filename of the file to insert.
  Returns:
    Inserted file metadata if successful, None otherwise.
  """
  if not folder:
    media_body = MediaFileUpload(filename, mimetype=mime_type, resumable=True)
  body = {
    'title': title,
    'description': description,
    'mimeType': mime_type
  }
  # Set the parent folder.
  if parent_id:
    body['parents'] = [{'id': parent_id}]

  try:
    if not folder:
        file = service.files().insert(
        body=body,
        media_body=media_body).execute()
    else:
        file = service.files().insert(
        body=body).execute()

    # Uncomment the following line to print the File ID
    print 'File ID: %s' % file['id']

    return file
  except errors.HttpError, error:
    print 'An error occured: %s' % error
    return None

def insert_permission(service, file_id, value=None, perm_type='anyone', role='writer'):
  """Insert a new permission.

  Args:
    service: Drive API service instance.
    file_id: ID of the file to insert permission for.
    value: User or group e-mail address, domain name or None for 'default'
           type.
    perm_type: The value 'user', 'group', 'domain' or 'default'.
    role: The value 'owner', 'writer' or 'reader'.
  Returns:
    The inserted permission if successful, None otherwise.
  """
  new_permission = {
      'value': value,
      'type': perm_type,
      'role': role
  }
  try:
    return service.permissions().insert(
        fileId=file_id, body=new_permission).execute()
  except errors.HttpError, error:
    print 'An error occurred: %s' % error
  return None

def retrieve_all_files(service):
  """Retrieve a list of File resources.

  Args:
    service: Drive API service instance.
  Returns:
    List of File resources.
  """
  result = []
  page_token = None
  while True:
    try:
      param = {}
      if page_token:
        param['pageToken'] = page_token
      files = service.files().list(**param).execute()

      result.extend(files['items'])
      page_token = files.get('nextPageToken')
      if not page_token:
        break
    except errors.HttpError, error:
      print 'An error occurred: %s' % error
      break
  return result