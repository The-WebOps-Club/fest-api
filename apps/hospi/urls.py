from django.conf.urls import patterns, url

urlpatterns = patterns('',
    # For mainsite
    url(r'^$', 'apps.hospi.views.prehome', name='hospi_prehome'),
    url(r'^home/(?P<team_id>\d+)/$', 'apps.hospi.views.home', name='hospi_home'),
    url(r'^login/$', 'apps.hospi.views.login', name='hospi_login'),
    url(r'^logout/$', 'apps.hospi.views.logout', name='hospi_logout'),
    url(r'^add_members/$', 'apps.hospi.views.add_members', name='hospi_add_members'),
    url(r'^del_member/(?P<team_id>\d+)/(?P<member_id>\d+)/$', 'apps.hospi.views.delete_member', name='hospi_del_member'),
    url(r'^add_accomod/$', 'apps.hospi.views.add_accomodation', name='hospi_add_accomodation'),
    url(r'^saar/(?P<team_id>\d+)/$', 'apps.hospi.views.generate_saar', name='hospi_saar'),
    url(r'^add/team/$', 'apps.hospi.views.user_add_team', name='hospi_user_add_team'),
    url(r'^save/team/$', 'apps.hospi.views.user_save_team', name='hospi_user_save_team'),
    url(r'^set/hospi/(?P<team_id>\d+)/$', 'apps.hospi.views.set_hospi_team', name='hospi_set_hospi_team'),
    url(r'^set/event/(?P<event_team_id>\d+)/$', 'apps.hospi.views.set_event_team', name='hospi_set_event_team'),
    url(r'^details/(?P<team_id>\d+)/$', 'apps.hospi.views.details', name='hospi_details'),
    url(r'^cancel/(?P<team_id>\d+)/$', 'apps.hospi.views.cancel_request', name='hospi_cancel_request'),
    url(r'^delete/(?P<team_id>\d+)/$', 'apps.hospi.views.delete_team', name='delete_team'),

    # For ERP
    # url(r'^admin/$', 'hospi.views.list_registered_teams', name='hospi_list_registered_teams'),
    url(r'^admin/details/(?P<team_id>\d+)/$', 'apps.hospi.views.team_details', name='hospi_team_details'),
    # url(r'^admin/update/(?P<team_id>\d+)/$', 'hospi.views.update_status', name='hospi_update_status'),
    # url(r'^admin/statistics/$', 'hospi.views.statistics', name='hospi_statistics'),
    # url(r'^admin/add/$', 'hospi.views.add_hostel_rooms', name='hospi_add_hostel_rooms'),
    # url(r'^admin/add/hostel/$', 'hospi.views.add_hostel', name='hospi_add_hostel'),
    # url(r'^admin/add/room/$', 'hospi.views.add_room', name='hospi_add_room'),
    # url(r'^admin/rooms/$', 'hospi.views.room_map', name='hospi_room_map'),
    # url(r'^admin/hostel/(?P<hostel_id>\d+)/$', 'hospi.views.hostel_details', name='hospi_hostel_details'),
    # url(r'^admin/room/(?P<room_id>\d+)/$', 'hospi.views.room_details', name='hospi_room_details'),
    # url(r'^admin/all_teams/$', 'hospi.views.list_all_teams', name='hospi_list_all_teams'),
    # url(r'^admin/add/team/$', 'hospi.views.add_team', name='hospi_add_team'),
    # url(r'^admin/save/team/$', 'hospi.views.save_team', name='hospi_save_team'),
    # url(r'^admin/check_in/(?P<team_id>\d+)/$', 'hospi.views.check_in_team', name='hospi_check_in_team'),
    # url(r'^admin/check_in_mixed/$', 'hospi.views.check_in_mixed', name='hospi_check_in_mixed'),
    # url(r'^admin/check_in_males/$', 'hospi.views.check_in_males', name='hospi_check_in_males'),
    # url(r'^admin/check_in_females/$', 'hospi.views.check_in_females', name='hospi_check_in_females'),
    # url(r'^admin/check_out/(?P<team_id>\d+)/$', 'hospi.views.check_out_team', name='hospi_check_out_team'),

    # url(r'^admin/update_member/$', 'hospi.views.update_member', name='hospi_update_member'),
    # url(r'^admin/add_member/(?P<team_id>\d+)/$', 'hospi.views.add_member', name='hospi_add_member'),
    # url(r'^admin/del_member/(?P<team_id>\d+)/$', 'hospi.views.del_member', name='hospi_del_member'),

    # url(r'^admin/web_id_search/$', 'hospi.views.website_id_search', name='hospi_website_id_search'),
    # url(r'^admin/add_user/$', 'hospi.views.add_user_to_team', name='hospi_add_user_to_team'),

    # url(r'^admin/split/(?P<team_id>\d+)/$', 'hospi.views.split_team', name='hospi_split_team'),
    # url(r'^admin/print/(?P<team_id>\d+)/$', 'hospi.views.print_bill', name='hospi_print_bill'),
    url(r'^admin/print_saar/(?P<team_id>\d+)/$', 'apps.hospi.views.print_saar', name='hospi_print_saar'),
    # url(r'^admin/delete/(?P<room_id>\d+)/$', 'hospi.views.delete_room', name='hospi_delete_room'),

    )
