# Authorise machine

from django.core.management.base import BaseCommand, CommandError, NoArgsCommand
from django.conf import settings

from apps.docs.models import CredentialsModel
from apps.docs.api import create_flow

import json

from oauth2client.client import OAuth2WebServerFlow

class Command(BaseCommand):
    help = 'Retrieves the drive credentials. Make sure that Google API user is defined in settings \
    Arguments: either authorize or initialize'

    def handle(self, arg=None, **options):

        self.stdout.write("Parameter got : " + str(arg))
        if arg == "authorize":
            with open(settings.GOOGLE_API_CLIENT_SECRETS, 'r') as file:
                data = json.loads(''.join(file.readlines()).replace('\n',''))
            CLIENT_ID = data['web']['client_id']
            CLIENT_SECRET = data['web']['client_secret']
            OAUTH_SCOPE = ' '.join(settings.GOOGLE_API_SCOPES)
            flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE, settings.GOOGLE_API_REDIRECT_URI)
            flow.params['access_type'] = 'offline'
            flow.params['approval_prompt'] = 'force'
            authorize_url = flow.step1_get_authorize_url()
            print 'Go to the following link in your browser: LOGIN AS '+ settings.GOOGLE_API_USER_EMAIL + authorize_url
            code = raw_input('Enter verification code: ').strip()
            credentials = flow.step2_exchange(code)
            print credentials.to_json()
            storage = CredentialsModel.objects.get_or_create(identifier=settings.GOOGLE_API_USER_EMAIL)
            storage = storage[0]
            storage.credential = credential.to_json()
            storage.refresh_token = credential.refresh_token
            storage.save()
            self.stdout.write("\nSave this as GOOGLE_API_CREDENTIALS in settings.py\n\n" + str(credential.to_json()))
            return
        elif arg == 'initialize':
            pass
        else:
            self.stdout.write("Invalid argument. Accepted arguments = 'authorize', 'initialize'" )
                    
