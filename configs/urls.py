# Django
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
# Apps
# Decorators
# Models
# Forms
# View functions
# Misc
from misc.utils import *  #Import miscellaneous functions
import notifications
import social
# Python

# Admin
admin.autodiscover()

# Dajax
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()

#django push notifications
from push_notifications.models import GCMDevice
from rest_framework.generics import ListCreateAPIView

# REST API
from rest_framework.routers import DefaultRouter
from apps.api import mobile, gcm


router = DefaultRouter()
router.register(r'notifications', mobile.NotificationViewSet, base_name="notifications")
router.register(r'walls',mobile.WallsViewSet, base_name="walls")
router.register(r'posts',mobile.PostsViewSet, base_name="posts")
router.register(r'comments',mobile.CommentsViewSet, base_name="comments")
router.register(r'gcm',gcm.GCMViewSet, base_name="gcm")
router.register(r'profile',mobile.UserProfileViewSet,base_name="profile")

urlpatterns = patterns('',
    # ------------------------------------------------------------------
    # FEST-API APPS
    url(r'^$', 'apps.home.views.home', name='home'),
    url(r'^markdown$', 'apps.home.views.markdown', name='markdown'),    

    # Users
    url(r'^login/$', 'apps.users.views.login_user', name='login'), # Logs user in
    url(r'^first_login_required/$', 'apps.users.views.first_login_required', name='first_login_required'), # Gives error message if first_login
    url(r'^associate/$', 'apps.users.views.associate', name='associate'), # Asks for associations
    url(r'^profile/(?P<user_id>\d+)$', 'apps.users.views.profile', name='profile'), # Shows profile page of user
    url(r'^profile$', 'apps.users.views.profile', name='profile'),
    url(r'^identity/(?P<role_type>\w+)/(?P<role_id>\d+)$', 'apps.users.views.identity', name='identity'), # Changes identity of the user
    url(r'^identity$', 'apps.users.views.identity', name='identity'),
    # Email unsubscribe
    url(r'^unsubscribe/(?P<username>[\w.@+-]+)/(?P<token>[\w.:\-_=]+)/$', 'apps.users.views.unsubscribe'),
    # Home
    url(r'^newsfeed/$', 'apps.home.views.newsfeed', name='newsfeed'), # Shows newsfeed for a user
    url(r'^contacts/$', 'apps.home.views.contacts', name='contacts'), # Shows contact page
    
    # Notification
	url(r'^notification/read/(?P<notif_id>\w+)$', 'apps.home.views.read_notification', name='read_notification'), # makes the given notification read and redirects to the page
	
	# Walls
    url(r'^wall/(?P<wall_id>\d+)$', 'apps.walls.views.wall', name='wall'),
    url(r'^wall/(?P<wall_id>\d+)/(?P<post_id>\d+)$', 'apps.walls.views.wall', name='wall'),
    url(r'^wall$', 'apps.walls.views.wall', name='wall'),
    url(r'^wall/(?P<owner_type>\w+)/(?P<owner_id>\d+)$', 'apps.walls.views.my_wall', name='my_wall'),
    
    # Docs
    url(r'^docs/$', 'apps.docs.views.docs', name='docs'),
    url(r'^docs/picker/?$', 'apps.docs.views.picker', name='picker'),
    url(r'^docs/view/$', 'apps.docs.views.edit_file', name='view'),
    # Internal URLS - One time use
    url(r'^google/refresh_token$', 'apps.docs.views.google_refresh_token', name='google_refresh_token'),
    url(r'^google/oauth2callback/?$', 'apps.docs.views.google_auth_callback', name='google_oauth2callback'),
	url(r'^github/refresh_token$', 'apps.docs.views.github_refresh_token', name='github_refresh_token'),
    url(r'^github/oauth2callback/?$', 'apps.docs.views.github_auth_callback', name='github_oauth2callback'),

    # Misc
    url(r'^show/404/$', 'misc.views.err404',  name='err404'),
    url(r'^show/500/$', 'misc.views.err500',  name='err505'),
    #url(r'^setup/$', 'misc.views.setup', name='setup'),

    url(r'^portals/admin/$','apps.portals.general.views.admin_portal', name='admin_portal' ),
    url(r'^portals/finance/$','apps.portals.finance.views.finance_portal', name='finance_portal' ),
    url(r'^portals/events/$','apps.portals.events.views.portal_main', name='events_portal'),

    #Event Tabs (backend only)
    url(r'^events/add_tabs/$','apps.events.views.add_tabs', name='add_tabs'),

    # Participant - Login/registration
    url(r'^participant_registration/$','apps.users.views.participant_registration', name='participant_registration'),
    url(r'^participant_login/$','apps.users.views.participant_login', name='participant_login'),
    
    # ------------------------------------------------------------------
    # DJANGO APPS - FOR EXTERNAL USE
    
    # ------------------------------------------------------------------
    # DJANGO APPS
    # Admin
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    
    #Auth
    url(r'^logout/?$', 'django.contrib.auth.views.logout', {'next_page':settings.SITE_URL}, name='logout'),
    url(r'^password_reset/$', 'django.contrib.auth.views.password_reset', {'template_name':'password/reset.html', 'extra_context':{'FEST_NAME':settings.FEST_NAME,}}, name='password_reset'),
    url(r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done',{'template_name':'password/reset_done.html', 'extra_context':{'FEST_NAME':settings.FEST_NAME,}}, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 'django.contrib.auth.views.password_reset_confirm', {'template_name':'password/reset_new_password.html', 'extra_context':{'FEST_NAME':settings.FEST_NAME,}}, name='password_reset_confirm'),
    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete',{'template_name':'password/reset_complete.html', 'extra_context':{'FEST_NAME':settings.FEST_NAME,}}, name='password_reset_complete'),

    # ------------------------------------------------------------------
    # THIRD PARTY APPS
    # Dajaxice
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    
    # Notifications
    url(r'^inbox/notifications/', include(notifications.urls)),
    
    # Python social auth
    url(r'', include('social.apps.django_app.urls', namespace='social')),
    
    # Haystack
    url(r'^search/', include('haystack.urls')),

    #For Testing out email templates
    url(r'^email/$', 'apps.walls.views.email_test', name='email'),
    #For Testing out api
    url(r'^apitest/$', 'apps.walls.views.api_test', name='apitest'),

    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT}),

    # API
    url(r'^api-web-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', 'rest_framework.authtoken.views.obtain_auth_token'),
    url(r'^api/mobile/', include(router.urls)),
    url(r'^api-docs/', include('rest_framework_swagger.urls')),

)

# 400 & 500
handler404 = 'misc.views.err404'
handler500 = 'misc.views.err500'

# This is to test out DEBUG = False in localhost
# REMEMBER : Should be commented out on server !
# if settings.DEBUG or ( ( settings.SITE_URL.find("localhost") != -1 or settings.SITE_URL.find("127.0.") != -1 ) and not settings.DEBUG ):
#urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     # Explicit settings patch for debug_toolbar for Django 1.6
#     # http://django-debug-toolbar.readthedocs.org/en/1.0/installation.html#explicit-setup
#     import debug_toolbar
#     urlpatterns += patterns('',
#         url(r'^__debug__/', include(debug_toolbar.urls)),
#     )

skip_last_activity_date = [
    # Your expressions go here ... for LastActivityDatabaseMiddleware
]

