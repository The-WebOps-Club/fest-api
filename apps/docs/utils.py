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
# Forms
# View functions
# Misc
# Python
import httplib2, json

class Drive:
    service = None

    def __init__(self):
        """
            Initializer for Drive class
            Args: None
            Returns: Authenticated drive service object
        """
        # try:
        if not settings.GOOGLE_API_CREDENTIALS or settings.GOOGLE_API_CREDENTIALS == "":
            print ">>> ERR >>> GOOGLE_API_CREDENTIALS not defined"
        credential = Credentials.new_from_json(settings.GOOGLE_API_CREDENTIALS)
        # except Exception, e:
        #     return redirect('get_refresh_token')
        http = httplib2.Http()
        http = credential.authorize(http)
        self.service = build('drive', 'v2', http=http)

    def create_flow(self):
        FLOW = flow_from_clientsecrets(
                settings.GOOGLE_API_CLIENT_SECRETS, 
                ' '.join(settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE), 
                redirect_uri=settings.GOOGLE_API_REDIRECT_URI
        )
        FLOW.params['access_type'] = 'offline'
        FLOW.params['approval_prompt'] = 'force'
        return FLOW
    
    def insert_file(self, title, description, parent_id, mime_type, filename, folder=False):
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
                    file = self.service.files().insert(
                    body = body,
                    media_body = media_body).execute()
            else:
                    file = self.service.files().insert(
                    body=body).execute()

            # Uncomment the following line to print the File ID
            print 'File ID: %s' % file['id']

            return file
        except errors.HttpError, error:
            print 'An error occured: %s' % error
            return None

    def set_permission(self, file_id, value=None, perm_type='anyone', role='writer'):
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
        if perm_type not in ["user", "group", "domain", "anyone"]:
            raise InvalidArgumentValueException("Permission TYpe was found to be : " + str(perm_type))

        new_permission = {
                'value': value,
                'type': perm_type,
                'role': role
        }
        try:
            return self.service.permissions().insert(
                fileId = file_id, 
                body = new_permission
            ).execute()
        except errors.HttpError, error:
            print 'An error occurred: %s' % error
        return None

    def retrieve_all_files(self):
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
                files = self.service.files().list(**param).execute()

                result.extend(files['items'])
                page_token = files.get('nextPageToken')
                if not page_token:
                    break
            except errors.HttpError, error:
                print 'An error occurred: %s' % error
                break
        return result

def create_flow():
    FLOW = flow_from_clientsecrets(
        settings.GOOGLE_API_CLIENT_SECRETS, 
        ' '.join(settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE), 
        redirect_uri=settings.GOOGLE_API_REDIRECT_URI
    )
    FLOW.params['access_type'] = 'offline'
    FLOW.params['approval_prompt'] = 'force'
    return FLOW

def get_access_token():
        if not settings.GOOGLE_API_CREDENTIALS or settings.GOOGLE_API_CREDENTIALS == "":
            print ">>> ERR >>> GOOGLE_API_CREDENTIALS not defined"
        credential = Credentials.new_from_json(settings.GOOGLE_API_CREDENTIALS)
        http = httplib2.Http()
        credential._refresh(http.request)
        return credential.access_token
