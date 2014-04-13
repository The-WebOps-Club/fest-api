from django.conf.urls import patterns, url

urlpatterns = patterns('',
    # For mainsite
    url(r'^$', 'apps.docs.views.docs', name='docs'),
    url(r'^oauth2callback/?$', 'apps.docs.views.oauth2callback', name='oauth2callback'),
    )
