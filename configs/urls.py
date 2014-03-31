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
    url(r'^login/$', 'apps.users.views.login_user', name='login'),
    url(r'^profile/(?P<user_id>\d+)$', 'apps.users.views.profile', name='profile'),
    url(r'^profile$', 'apps.users.views.profile', name='profile'),
    url(r'^identity/(?P<role_type>\w+)/(?P<role_id>\d+)$', 'apps.users.views.identity', name='identity'),
    url(r'^identity$', 'apps.users.views.identity', name='identity'),
    url(r'^show/login/$', 'apps.users.views.show_login_user'),
    url(r'^show/profile/$', 'apps.users.views.show_profile'),

    # Home
    url(r'^newsfeed/$', 'apps.home.views.newsfeed', name='newsfeed'),
    url(r'^norifications/$', 'apps.home.views.notifications', name='notifications'),
    url(r'^show/newsfeed/$', 'apps.home.views.show_newsfeed'),

    # Walls
    url(r'^wall/(?P<wall_id>\d+)$', 'apps.walls.views.wall', name='wall'),
    url(r'^wall$', 'apps.walls.views.wall', name='wall'),
    url(r'^create_post/(?P<wall_id>\d+)/$', 'apps.walls.views.create_post',  name='create_post'),
    url(r'^create_comment/(?P<post_id>\d+)/$', 'apps.walls.views.create_comment',  name='create_comment'),
    url(r'^show/wall/$', 'apps.walls.views.show_wall'),
    
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
    
    # ------------------------------------------------------------------
    # THIRD PARTY APPS
    # Dajaxice
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    # Notifications
    url(r'^inbox/notifications/', include(notifications.urls)),
    # Python social auth
    url(r'', include('social.apps.django_app.urls', namespace='social'))

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
