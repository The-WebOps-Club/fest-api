# Django
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
# Apps
from misc.utils import *  #Import miscellaneous functions
# Decorators
# Models
# Forms
# View functions
# Misc
# Python

# Admin
admin.autodiscover()

urlpatterns = patterns('',
    # ------------------------------------------------------------------
    # FEST-API APPS
    url(r'^admin/', include(admin.site.urls)),
    
    # ------------------------------------------------------------------
    # DJANGO APPS - FOR EXTERNAL USE
    
    # ------------------------------------------------------------------
    # DJANGO APPS
    # Admin
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # ------------------------------------------------------------------
    # THIRD PARTY APPS

)

# 400 & 500
handler404 = 'misc.views.err404'
handler500 = 'misc.views.err500'

# This is to test out DEBUG = False in localhost
# REMEMBER : Should be commented out on server !
if settings.DEBUG or ( ( settings.SITE_URL.find("localhost") != -1 or settings.SITE_URL.find("127.0.") != -1 ) and not settings.DEBUG ):
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
