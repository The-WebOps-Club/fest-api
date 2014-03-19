from django.conf.urls import patterns, url
urlpatterns = patterns('',
    
    url(r'^login/$', 'apps.users.views.login_user', name='login'),
    
)