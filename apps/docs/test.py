#!/usr/bin/python

import httplib2
import pprint

from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow

# Copy your credentials from the APIs Console
CLIENT_ID = '46389932382-ja94ulqb30qaqbdhuak1391iskutpf4k.apps.googleusercontent.com'
CLIENT_SECRET = '2RS-SCar6_YPtmUeZ1Eqgzqt'
REDIRECT_URL = 'http://localhost:8000/docs/oauth2callback'
# Check https://developers.google.com/drive/scopes for all available scopes
OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'

# Path to the file to upload
FILENAME = 'document.txt'

    # Run through the OAuth flow and retrieve credentials
flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE)
flow.params['access_type'] = 'offline'
flow.params['approval_prompt'] = 'force'
authorize_url = flow.step1_get_authorize_url()
# return authorize_url

print 'Go to the following link in your browser: ' + authorize_url
code = raw_input('Enter verification code: ').strip()
credentials = flow.step2_exchange(code)
print credentials.to_json()

    # Create an httplib2.Http object and authorize it with our credentials
http = httplib2.Http()
http = credentials.authorize(http)

drive_service = build('drive', 'v2', http=http)

    # Insert a file
media_body = MediaFileUpload(FILENAME, mimetype='text/plain', resumable=True)
body = {
    'title': 'My document',
    'description': 'A test document',
    'mimeType': 'text/plain'
}

file = drive_service.files().insert(body=body, media_body=media_body).execute()
pprint.pprint(file)
