import os, sys, django
gettext = lambda s: s

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'hz3@sbz0q+wb&irbyn0h)cu9+9t7ofh@1tn3s!^)xia8_u$2+4' # Good practice to have one more in local settings

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = DEBUG
DAJAXICE_DEBUG = DEBUG

PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
PYTHON_VERSION = '%s.%s' % sys.version_info[:2]
DJANGO_VERSION = django.get_version()

ALLOWED_HOSTS = ['*']

#Absolute URL where the site has been hosted. Don't forget the trailing slash.
SITE_URL = 'http://localhost:8000/'

# -------------------------------------------------------------------
# Apps
DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)
THIRD_PARTY_APPS = (
    # For development ease of use
    'south',
    'debug_toolbar',
    'django_extensions',
    'django_pdb',
    
    # ajax functionality
    'dajaxice',
    'dajax',
    
    # For programming ease
    'post_office',
)
API_APPS =(
    'misc',
    'apps.home', 
    'apps.users',
    'apps.walls',
    'apps.events',
    
)
INSTALLED_APPS =  DJANGO_APPS + THIRD_PARTY_APPS + API_APPS

# -------------------------------------------------------------------
# Various configs
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.messages.context_processors.messages',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.csrf',
)
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend', # default
    'apps.users.backends.RootBackend', # custom default password
)

ROOT_URLCONF = 'configs.urls'
WSGI_APPLICATION = 'configs.wsgi.application'

# Explicit settings patch for debug_toolbar for Django 1.6
# http://django-debug-toolbar.readthedocs.org/en/1.0/installation.html#explicit-setup
# DEBUG_TOOLBAR_PATCH_SETTINGS = False

# AUTH_PROFILE_MODULE = 'apps.users.models.ERPUser'
# Database
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(PROJECT_PATH, 'db.sqlite3'),
#    }
#}

# -------------------------------------------------------------------
# Internationalization
LANGUAGE_CODE = 'en-IN'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_L10N = True
USE_TZ = True
DATE_FORMAT = 'N j, Y'
DATETIME_FORMAT = 'P, N j, Y'
TIME_FORMAT = '%H:%M'

# -------------------------------------------------------------------
# Paths for static, media and templates
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_PATH, "files", "static-collected")
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(PROJECT_PATH, "files", "media")
STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, "files", "static"),
)
TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, "templates"),
)

# -------------------------------------------------------------------
# To disable suspicious operation error messages
def skip_suspicious_operations(record):
    if record.exc_info:
        exc_value = record.exc_info[1]
        if isinstance(exc_value, SuspiciousOperation):
            return False
    return True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        # Define filter for suspicious operations
        'skip_suspicious_operations': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': skip_suspicious_operations,
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false', 'skip_suspicious_operations'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# Settings for specific Apps
# Post Office
EMAIL_BACKEND = 'post_office.EmailBackend'
