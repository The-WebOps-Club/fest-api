import global_settings
from global_settings import *

# Add the Secret Key (Large Random String) to files/secret/key.txt
with open(os.path.join(BASE_DIR, "files", "secret") + 'key.txt') as f:
    SECRET_KEY = f.read().strip()
    
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
        'NAME': 'fest-api-db-name',
        'USER': 'user',
        'PASSWORD': 'password',
        'HOST': '',
        'PORT': '',
    }
}

ALLOWED_HOSTS = [
    '.example.com', # Allow domain and subdomains
]

# Email configurations
SEND_EMAIL = True
DEFAULT_FROM_EMAIL = 'Fest-API <noreply@festapi.com>'
SERVER_EMAIL = 'Fest-API Server <server@festapi.com>' #The email address that error messages come from, such as those sent to ADMINS and MANAGERS.