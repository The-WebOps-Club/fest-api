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

urlpatterns = patterns('',
    # ------------------------------------------------------------------
    # FEST-API APPS
    url(r'^$', 'apps.home.views.home', name='home'),

    # Users
    url(r'^login/$', 'apps.users.views.login_user', name='login'), # Logs user in
    url(r'^associate/$', 'apps.users.views.associate', name='associate'), # Logs user in
    url(r'^profile/(?P<user_id>\d+)$', 'apps.users.views.profile', name='profile'), # Shows profile page of user
    url(r'^profile$', 'apps.users.views.profile', name='profile'),
    url(r'^identity/(?P<role_type>\w+)/(?P<role_id>\d+)$', 'apps.users.views.identity', name='identity'), # Changes identity of the user
    url(r'^identity$', 'apps.users.views.identity', name='identity'),
    
    # Home
    url(r'^newsfeed/$', 'apps.home.views.newsfeed', name='newsfeed'), # Shows newsfeed for a user
    url(r'^notifications/$', 'apps.home.views.notifications', name='notifications'), # Shows all notifications for a user
    url(r'^contacts/$', 'apps.home.views.contacts', name='contacts'), # Shows contact page
    url(r'^markdown/$', 'apps.home.views.markdown', name='markdown'), # Shows markdown page
    
    # Notification
	url(r'^notification/read/(?P<notif_id>\w+)$', 'apps.home.views.read_notification', name='read_notification'), # makes the given notification read and redirects to the page
	
	# Walls
    url(r'^wall/(?P<wall_id>\d+)$', 'apps.walls.views.wall', name='wall'),
    url(r'^wall$', 'apps.walls.views.wall', name='wall'),
    url(r'^wall/(?P<owner_type>\w+)/(?P<owner_id>\d+)$', 'apps.walls.views.my_wall', name='my_wall'),
    url(r'^create_post/(?P<wall_id>\d+)/$', 'apps.walls.views.create_post',  name='create_post'),
    url(r'^create_comment/(?P<post_id>\d+)/$', 'apps.walls.views.create_comment',  name='create_comment'),
    
    # Docs
    url(r'^docs/$', 'apps.docs.views.docs', name='docs'),
    url(r'^docs/refresh_token$', 'apps.docs.views.get_refresh_token', name='get_refresh_token'),
    url(r'^docs/oauth2callback/?$', 'apps.docs.views.auth_callback', name='oauth2callback'),
    url(r'^docs/upload/?$', 'apps.docs.views.upload_a_file', name='upload'),
    url(r'^docs/init/?$', 'apps.docs.views.initialise_drive', name='init'),
    url(r'^docs/picker/?$', 'apps.docs.views.picker', name='picker'),


    # Misc
    url(r'^show/404/$', 'misc.views.err404',  name='err404'),
    url(r'^show/500/$', 'misc.views.err500',  name='err505'),

    # ------------------------------------------------------------------
    # DJANGO APPS - FOR EXTERNAL USE
    
    # ------------------------------------------------------------------
    # DJANGO APPS
    # Admin
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    
    #Auth
    url(r'^logout/?$', 'django.contrib.auth.views.logout', {'next_page':'/'}, name='logout'),
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
    
)

# 400 & 500
handler404 = 'misc.views.err404'
handler500 = 'misc.views.err500'

# This is to test out DEBUG = False in localhost
# REMEMBER : Should be commented out on server !
# if settings.DEBUG or ( ( settings.SITE_URL.find("localhost") != -1 or settings.SITE_URL.find("127.0.") != -1 ) and not settings.DEBUG ):
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     # Explicit settings patch for debug_toolbar for Django 1.6
#     # http://django-debug-toolbar.readthedocs.org/en/1.0/installation.html#explicit-setup
#     import debug_toolbar
#     urlpatterns += patterns('',
#         url(r'^__debug__/', include(debug_toolbar.urls)),
#     )
