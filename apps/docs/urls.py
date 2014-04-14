from django.conf.urls import patterns, url

urlpatterns = patterns('',
    # # For mainsite
    url(r'^$', 'apps.docs.views.docs', name='docs'),
    url(r'^refresh_token$', 'apps.docs.views.get_refresh_token', name='get_refresh_token'),
    url(r'^oauth2callback/?$', 'apps.docs.views.auth_callback', name='oauth2callback'),
    url(r'^upload/?$', 'apps.docs.views.upload_a_file', name='upload'),
    url(r'^init/?$', 'apps.docs.views.initialise_drive', name='init'),

    )
