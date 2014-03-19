from django.conf.urls import patterns, url
urlpatterns = patterns('',
    
    url(r'^login/$', 'apps.users.views.login', name='login'),

)

from django.conf.urls import patterns, include, url


# urlpatterns = patterns('',
#     url(r'^$', 'main.views.home', name='main_home'),
#     url(r'^register/(?P<eventId>\d+)/$', 'main.views.register', name='register'),
#     url(r'^register/csrf/$', 'main.views.get_csrf', name='get_csrf'),
#     url(r'^register_team/(?P<eventId>\d+)/(?P<teamId>\d+)/$', 'main.views.register_team', name='register_team'),
#     url(r'^list_teams/(?P<eventId>\d+)/$', 'main.views.list_teams', name='list_teams'),
#     url(r'^register/new/$', 'main.views.new_profile', name='register_new_user'),
#     url(r'^create_team/(?P<eventId>\d+)/$', 'main.views.create_team', name='create_team'),
#     url(r'^band_details/(?P<eventId>\d+)/(?P<teamId>\d+)/$', 'main.views.band_details', name='band_details'),

#     url(r'^login/$', 'main.views.login', name='main_login'),
#     url(r'^logout/$', 'main.views.logout', name='main_logout'),
#     url(r'^check/$', 'main.views.check_login_status', name='main_check'),
#     url(r'^profile/$', 'main.views.profile', name='main_profile'),

#     url(r'^fmi/$', 'main.views.fmi', name='main_fmi'),
#     url(r'^tfi/$', 'main.views.tfi', name='main_tfi'),
#     url(r'^feedback/$', 'main.views.feedback', name='main_feedback'),

#     url(r'^forgot/$', 'main.views.forgot_password', name='main_forgot_password'),
#     url(r'^reset/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 'main.views.reset_password', name='main_reset_password'),

#     url(r'^spons/$', 'main.views.spons_page', name='main_spons_page'),

#     url(r'^activate/(?P<email>.+)/$', 'main.views.check_account', name='main_check_account'),

# )