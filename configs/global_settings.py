import os, sys, django, random, re
#import apps.walls.utils

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

PERMISSION_COMMAND = False
#Absolute URL where the site has been hosted. Don't forget the trailing slash.
SITE_URL = 'http://localhost:8000/'

LOGIN_URL = 'login'

# -------------------------------------------------------------------
# Apps
DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
)
THIRD_PARTY_APPS = (
    # For development ease of use
    'south',
    'debug_toolbar',
    'django_extensions',
    
    # ajax functionality
    'dajaxice',
    # 'dajax',
    
    # For programming ease
    'post_office',
    'annoying',

    # Notification
    'notifications',

    # Social Auth Login
    'social.apps.django_app.default',

    # Search Indexer
    #'haystack',

    # compressor - Easy to use minifier and cache system
    'compressor',

    # Celery - task scheduling
    # 'djcelery',

    # Simple stuff
    'exportdata', # used to generate csv files from models

    # Mobile and Mainsite API
    'rest_framework',
    'rest_framework.authtoken',
)
API_APPS = (
    'misc',
    'apps.home', 
    'apps.users',
    'apps.walls',
    #'apps.events',
    'apps.docs',
    'apps.webmirror',
    'apps.portals.events',
    'apps.portals.general',
    'apps.api',

)
INSTALLED_APPS =  DJANGO_APPS + THIRD_PARTY_APPS + API_APPS

# -------------------------------------------------------------------
# Various configs
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'dajaxice.finders.DajaxiceFinder',
    'compressor.finders.CompressorFinder',
)
MIDDLEWARE_CLASSES = (
    # Runs Last
    'annoying.middlewares.StaticServe',

    'django.middleware.cache.UpdateCacheMiddleware',
    
    'django.middleware.gzip.GZipMiddleware',
    #'htmlmin.middleware.HtmlMinifyMiddleware',
    
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    'apps.users.middleware.SocialAuthExceptionMiddleware',
    
    'django.middleware.cache.FetchFromCacheMiddleware',
    #'htmlmin.middleware.MarkRequestMiddleware',

    #'apps.users.middleware.LastActivityDatabaseMiddleware',
    #'apps.users.middleware.LastActivityCacheMiddleware',
    #'misc.middleware.ProfileMiddleware',

    # Runs first
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
    'apps.users.backends.EmailBackend', # email 
    'django.contrib.auth.backends.ModelBackend', # default
    'apps.users.backends.RootBackend', # custom default password
)

ROOT_URLCONF = 'configs.urls'
WSGI_APPLICATION = 'configs.wsgi.application'

# Explicit settings patch for debug_toolbar for Django 1.6
# http://django-debug-toolbar.readthedocs.org/en/1.0/installation.html#explicit-setup
# DEBUG_TOOLBAR_PATCH_SETTINGS = True

# AUTH_PROFILE_MODULE = 'apps.users.models.UserProfile'
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
DATE_INPUT_FORMATS = (
    # '%b %d %Y',       # 'Oct 25 2006'
    # '%b %d, %Y',      # 'Oct 25, 2006'
    # '%d %b %Y',       # '25 Oct 2006'
    '%d %b, %Y',      # '25 Oct, 2006'
    # '%B %d %Y',       # 'October 25 2006'
    '%B %d, %Y',      # 'October 25, 2006'
    # '%d %B %Y',       # '25 October 2006'
    # '%d %B, %Y',      # '25 October, 2006'
    # '%Y-%m-%d',       # '2006-10-25'
    '%d-%m-%Y',       # '10-25-2006'
    # '%m/%d/%Y',       # '10/25/2006'
    '%d/%m/%Y',       # '25/10/2006'
)

# -------------------------------------------------------------------
# Paths for static, media and templates
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_PATH, "files", "static-collected")
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(PROJECT_PATH, "files", "media")
EMAIL_ROOT = os.path.join(PROJECT_PATH, "files", "emails") # Contains email files for Post Office
DATA_ROOT = os.path.join(PROJECT_PATH, "files", "data") # Contains gen data files (used by some manage commands)
STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, "files", "static"), # Remember first element should be the user defined one.
    # used in management commands
)
TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, "files", "templates"),
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

# Cache systems
# ---------------------------------------------------
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211'
    }
}

# Settings for specific Apps
# ---------------------------------------------------

# ----------------------------------------------------
# FEST API SETTINGS
    # Last Activity Middleware
USER_ONLINE_TIMEOUT = 600 #=10mins # Number of seconds of inactivity before a user is marked offline
USER_LASTSEEN_TIMEOUT = 60 * 60 * 24 * 7 #=1week # Number of seconds that we will keep track of inactive users for before their last seen is removed from the cache
    # LITE MODE ON setting
EXPERIMENTAL_MODE = True

# Post Office
EMAIL_BACKEND = 'post_office.EmailBackend'
POST_OFFICE = {
    'BATCH_SIZE': 100
}
# Required cron job: * * * * * (/usr/bin/python manage.py send_queued_mail >> send_mail.log 2>&1)

# ---------------------------------------------------
# Python Social Auth
AUTHENTICATION_BACKENDS = (
    # 'social.backends.amazon.AmazonOAuth2',
    # 'social.backends.angel.AngelOAuth2',
    # 'social.backends.aol.AOLOpenId',
    # 'social.backends.appsfuel.AppsfuelOAuth2',
    # 'social.backends.behance.BehanceOAuth2',
    # 'social.backends.belgiumeid.BelgiumEIDOpenId',
    # 'social.backends.bitbucket.BitbucketOAuth',
    # 'social.backends.box.BoxOAuth2',
    # 'social.backends.clef.ClefOAuth2',
    # 'social.backends.coinbase.CoinbaseOAuth2',
    # 'social.backends.dailymotion.DailymotionOAuth2',
    # 'social.backends.disqus.DisqusOAuth2',
    # 'social.backends.douban.DoubanOAuth2',
    # 'social.backends.dropbox.DropboxOAuth',
    # 'social.backends.evernote.EvernoteSandboxOAuth',
    'social.backends.facebook.FacebookAppOAuth2',
    'social.backends.facebook.FacebookOAuth2',
    # 'social.backends.fedora.FedoraOpenId',
    # 'social.backends.fitbit.FitbitOAuth',
    # 'social.backends.flickr.FlickrOAuth',
    # 'social.backends.foursquare.FoursquareOAuth2',
    'social.backends.github.GithubOAuth2',
    'social.backends.google.GoogleOAuth',
    'social.backends.google.GoogleOAuth2',
    'social.backends.google.GoogleOpenId',
    # 'social.backends.google.GooglePlusAuth',
    # 'social.backends.instagram.InstagramOAuth2',
    # 'social.backends.jawbone.JawboneOAuth2',
    'social.backends.linkedin.LinkedinOAuth',
    'social.backends.linkedin.LinkedinOAuth2',
    # 'social.backends.live.LiveOAuth2',
    # 'social.backends.livejournal.LiveJournalOpenId',
    # 'social.backends.mailru.MailruOAuth2',
    # 'social.backends.mendeley.MendeleyOAuth',
    # 'social.backends.mendeley.MendeleyOAuth2',
    # 'social.backends.mixcloud.MixcloudOAuth2',
    # 'social.backends.odnoklassniki.OdnoklassnikiOAuth2',
    # 'social.backends.open_id.OpenIdAuth',
    # 'social.backends.openstreetmap.OpenStreetMapOAuth',
    # 'social.backends.orkut.OrkutOAuth',
    # 'social.backends.persona.PersonaAuth',
    # 'social.backends.podio.PodioOAuth2',
    # 'social.backends.rdio.RdioOAuth1',
    # 'social.backends.rdio.RdioOAuth2',
    # 'social.backends.readability.ReadabilityOAuth',
    # 'social.backends.reddit.RedditOAuth2',
    # 'social.backends.runkeeper.RunKeeperOAuth2',
    # 'social.backends.skyrock.SkyrockOAuth',
    # 'social.backends.soundcloud.SoundcloudOAuth2',
    'social.backends.stackoverflow.StackoverflowOAuth2',
    # 'social.backends.steam.SteamOpenId',
    # 'social.backends.stocktwits.StocktwitsOAuth2',
    # 'social.backends.stripe.StripeOAuth2',
    # 'social.backends.suse.OpenSUSEOpenId',
    # 'social.backends.thisismyjam.ThisIsMyJamOAuth1',
    # 'social.backends.trello.TrelloOAuth',
    # 'social.backends.tripit.TripItOAuth',
    # 'social.backends.tumblr.TumblrOAuth',
    # 'social.backends.twilio.TwilioAuth',
    'social.backends.twitter.TwitterOAuth',
    # 'social.backends.vk.VKOAuth2',
    # 'social.backends.weibo.WeiboOAuth2',
    # 'social.backends.xing.XingOAuth',
    # 'social.backends.yahoo.YahooOAuth',
    # 'social.backends.yahoo.YahooOpenId',
    # 'social.backends.yammer.YammerOAuth2',
    # 'social.backends.yandex.YandexOAuth2',
    # 'social.backends.vimeo.VimeoOAuth1',
    # 'social.backends.lastfm.LastFmAuth',
    'social.backends.email.EmailAuth',
    'social.backends.username.UsernameAuth',
    'django.contrib.auth.backends.ModelBackend',
    'apps.users.backends.RootBackend', 
)

SOCIAL_AUTH_STRATEGY            = 'social.strategies.django_strategy.DjangoStrategy'
SOCIAL_AUTH_STORAGE             = 'social.apps.django_app.default.models.DjangoStorage'

# SOCIAL_AUTH_LOGIN_ERROR_URL = '/login-error/'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/login/'
# SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/profile/new'
# SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL = '/new-assoc/'
# SOCIAL_AUTH_DISCONNECT_REDIRECT_URL = '/account-disconnected/'
# SOCIAL_AUTH_RAISE_EXCEPTIONS = False
# SOCIAL_AUTH_ASSOCIATE_BY_MAIL = True
# SOCIAL_AUTH_COMPLETE_URL_NAME  = 'socialauth_complete'
# SOCIAL_AUTH_ASSOCIATE_URL_NAME = 'socialauth_associate_complete'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.messages.context_processors.messages',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    # I added these.
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.csrf',
    # Social Auth
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
)
# SOCIAL_AUTH_DEFAULT_USERNAME = lambda: random.choice(['Darth-Vader', 'Obi-Wan-Kenobi', 'R2-D2', 'C-3PO', 'Yoda', 'Tony-Stark', 'Bruce-Wayne', 'Black-Widow', 'Eric-Lensher', 'Charles-Xavier', 'Logan'])
# SOCIAL_AUTH_UUID_LENGTH = 16
SOCIAL_AUTH_PROTECTED_USER_FIELDS = ['email',]
SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True
SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    # 'example.app.pipeline.require_email',
    # 'social.pipeline.mail.mail_validation',
    # 'social.pipeline.user.create_user',
    'apps.users.pipeline.check_existing_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
    
)
# Social auth - backend specific
    # Google
SOCIAL_AUTH_GOOGLE_CONSUMER_KEY          = ''
SOCIAL_AUTH_GOOGLE_CONSUMER_SECRET       = ''
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY            = '186928535147.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET         = 'N2LxEfSraUVwC79sn4aqtqFE'
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE           = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/userinfo.email'
    # 'https://www.googleapis.com/auth/plus.login',    
]

    # Facebook
SOCIAL_AUTH_FACEBOOK_KEY                = ''
SOCIAL_AUTH_FACEBOOK_SECRET             = ''
SOCIAL_AUTH_FACEBOOK_SCOPE              = [
    'public_profile',
    'email', # Email scope
    
    'user_friends',
    
    'user_about_me', 'user_activities', 'user_birthday', 
    'user_checkins', 'user_education_history', 'user_events', 
    'user_groups', 'user_hometown', 'user_interests', 
    'user_likes', 'user_location', 'user_notes', 'user_photos', 
    'user_status', 'user_subscriptions', 'user_videos', 
    'user_work_history', # User extended profile scope
    
    'friends_about_me', 'friends_activities', 'friends_birthday', 
    'friends_checkins', 'friends_education_history', 'friends_events', 
    'friends_groups', 'friends_hometown', 'friends_interests', 
    'friends_likes', 'friends_location', 'friends_notes', 'friends_photos', 
    'friends_status', 'friends_subscriptions', 'friends_videos', 
    'friends_work_history', # friends extended profile scope
    
    'read_friendlists', 'read_insights', 'read_requests',
    'user_online_presence', 'friends_online_presence', 
    # Extended Permissions scope
    
    'create_event', 'manage_friendlists', 'manage_notifications', 
    'publish_actions', 'publish_stream', # Extended permissions publish
]
SOCIAL_AUTH_FACEBOOK_EXTENDED_PERMISSIONS = SOCIAL_AUTH_FACEBOOK_SCOPE
    # Twitter
SOCIAL_AUTH_TWITTER_KEY                 = ''
SOCIAL_AUTH_TWITTER_SECRET              = ''
    # Linkedin
SOCIAL_AUTH_LINKEDIN_CONSUMER_KEY        = ''
SOCIAL_AUTH_LINKEDIN_CONSUMER_SECRET     = ''
    # Facebook
SOCIAL_AUTH_YAHOO_CONSUMER_KEY           = ''
SOCIAL_AUTH_YAHOO_CONSUMER_SECRET        = ''

# ---------------------------------------------------
# Django markdown
MARKDOWN_STYLES = {
    "internal_default": {
        "extras": {
            "code-friendly": None,
            "cuddled-lists": True,
        },
        "safe_mode": False,
    },
    "trusted": {
        "extras": {
            "code-friendly": None,
            "cuddled-lists": True,
        },
        "safe_mode": False,
    },
    "my_default": {
    	"link_patterns": [
            # Transform into links
            # (re.compile(r"recipe\s+#?(\d+)\b", re.I), r"http://code.activestate.com/recipes/\1/"),
            
            # Proper link Original : (re.compile(r"""(?i)\b(?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?])""", re.I), r"dddd<\1>"),
            # Customized :
            # (re.compile(r"""(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/))((?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\)){1,10})(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?])""", re.I), r"<\1\2...>")

            # Render copied links as links
			#(re.compile(r"^(http://\S+)", re.I), r"\1"),
            #(re.compile(r"\s(http://\S+)", re.I), r" \1"),
            #(re.compile(r"^(https://\S+)", re.I), r"\1"),
            #(re.compile(r"\s(https://\S+)", re.I), r" \1"),
            #(re.compile(r"^(www\.\S+)", re.I), r"\1"),
            #(re.compile(r"\s(www\.\S+)", re.I), r" \1"),

        ],
        "extras": {
            "code-friendly": None, # For coding pros
            "cuddled-lists": None, # Dont convert lists
            "demote-headers": 3, #
            "fenced-code-blocks": None, # For coding pros
            "footnotes" : None, # too complicated to use
            "header-ids" : None, # No hashtag links required
            "pyshell" : None, # python on erp -_-
            "smarty-pants" : True, # gen
            "wiki-tables" : None, # high funda - too complicated
            "link-patterns" : None,
        },
        "safe_mode": False,
    },
}

# -------------------------------------------------
# Compressor
COMPRESS_CSS_FILTERS = [
    'compressor.filters.template.TemplateFilter',
    'compressor.filters.cssmin.CSSMinFilter',
]
COMPRESS_JS_FILTERS = [
    'compressor.filters.template.TemplateFilter',
    'compressor.filters.jsmin.JSMinFilter',
]
COMPRESS_ENABLED = False

# -------------------------------------------------
# HTML Minify
HTML_MINIFY = False
KEEP_COMMENTS_ON_MINIFYING = False
# EXCLUDE_FROM_MINIFYING = ()

# --------------------------------------------------
# GOOGLE DRIVE DOCS
USE_EXTERNAL_SITES = True
GOOGLE_API_CLIENT_SECRETS = os.path.join(PROJECT_PATH, 'configs', 'docs_oauth2_credentials.json')
GOOGLE_API_PUBLIC_KEY = ''
GOOGLE_API_REDIRECT_URI = SITE_URL + 'google/oauth2callback'
GOOGLE_API_CREDENTIALS_FILE_PATH = os.path.abspath(os.path.join(PROJECT_PATH, "configs", "google_api_credentials.json" ) )
GOOGLE_API_CREDENTIALS = ''
GOOGLE_DRIVE_ROOT_FOLDER_ID = ''
GOGOLE_API_PUBLIC_KEY = ''

if os.path.exists(GOOGLE_API_CREDENTIALS_FILE_PATH):
    with open(GOOGLE_API_CREDENTIALS_FILE_PATH) as f:
        GOOGLE_API_CREDENTIALS = f.read()

# ----------------------------------------------------
# Solr-Haystach search settings
# HAYSTACK_CONNECTIONS = {
#     'default': {
#         'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
#         'URL': 'http://127.0.0.1:8983/solr'
#     },
# }
#DEFAULT_POST_PERMISSION_STACK = PostPermissionSubqueries.build_post_permissions_stack()

SEND_NOTIF_EMAILS = True

# API Preferences
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )

}
