import global_settings
from global_settings import *

# Add the Secret Key (Large Random String) to files/secret/key.txt
# SECRET_KEY = 'hz3@sbz0q+wb&irbyn0h)cu9+9t7ofh@1tn3s!^)xia8_u$2+4' # Keep a specific key for production
    
FEST_NAME = "Fest API"

# Debug settings, machine specific
DEBUG = True
TEMPLATE_DEBUG = DEBUG
DAJAXICE_DEBUG = DEBUG

# Emails to which admin mails are sent
ADMINS = (
#    ('John', 'john@example.com'),
)

MANAGERS = (
#    ('John', 'john@example.com'),
)

# Database settings, machine specific
DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.mysql',
        'NAME': 'fest-api-db-name',
        'USER': 'user',
        'PASSWORD': 'password',
        'HOST': '',
        'PORT': '',
    }
}

ALLOWED_HOSTS = [ # Allowed domain and subdomains
    '*', 
]

#Absolute URL where the site has been hosted. Don't forget the trailing slash.
SITE_URL = 'http://localhost:8000/'

# Email configurations
SEND_EMAIL = True
DEFAULT_FROM_EMAIL = 'Fest-API <noreply@festapi.com>'
SERVER_EMAIL = 'Fest-API Server <server@festapi.com>' #The email address that error messages come from, such as those sent to ADMINS and MANAGERS.

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = 'full_path_for_emails'

# Docs integration
GOOGLE_API_USER_EMAIL = 'festapi14@gmail.com'
GOOGLE_API_CREDENTIALS = ""
GOOGLE_DRIVE_ROOT_FOLDER_ID = "0B75xGGtqUve5NGlHM1E0TWtVbEE"

# Python social auth tokens - Ali
SOCIAL_AUTH_FORCE_FB				 = False
# SOCIAL_AUTH_FACEBOOK_KEY             = '398345720274389'
# SOCIAL_AUTH_FACEBOOK_SECRET          = 'fd6da85c30b673d399ea6e61180e35da'
# SOCIAL_AUTH_GOOGLE_OAUTH2_KEY        = '186928535147.apps.googleusercontent.com'
# SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET     = 'N2LxEfSraUVwC79sn4aqtqFE'
