import global_settings
from global_settings import *

# Add the Secret Key (Large Random String) to files/secret/key.txt
# SECRET_KEY = 'hz3@sbz0q+wb&irbyn0h)cu9+9t7ofh@1tn3s!^)xia8_u$2+4' # Keep a specific key for production
    
# Debug settings, machine specific
DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Emails to which admin mails are sent
ADMINS = (
    ('John', 'john@example.com'),
    ('Mary', 'mary@example.com')
)

MANAGERS = (
    ('John', 'john@example.com'),
    ('Mary', 'mary@example.com')
)

# Database settings, machine specific
DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.mysql',
        'NAME': 'fest-test',
        'USER': 'root',
        'PASSWORD': '1',
        'HOST': '',
        'PORT': '',
    }
}

ALLOWED_HOSTS = [
    '*', # Allow domain and subdomains
]

# Email configurations
SEND_EMAIL = True
DEFAULT_FROM_EMAIL = 'Fest-API <noreply@festapi.com>'
SERVER_EMAIL = 'Fest-API Server <server@festapi.com>' #The email address that error messages come from, such as those sent to ADMINS and MANAGERS.
