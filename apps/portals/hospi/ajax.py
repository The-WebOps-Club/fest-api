# For rendering templates
from django.template import RequestContext
from django.template.loader import render_to_string
import json
from apps.hospi.models import HospiTeam, Hostel, Room, Allotment, HospiLog
from apps.hospi.forms import HostelForm, RoomForm, HospiTeamForm
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form

@dajaxice_register
def list_all_teams(request):
	dept_list= ['hospi', 'webops']
	teams = HospiTeam.objects.all()
	to_return = {
		'teams':teams,
	}
	html_content = render_to_string('portals/hospi/registered_teams.html', to_return, RequestContext(request))
	return json.dumps({'html_content':html_content})

@dajaxice_register
def accomodation_statistics(request):
    teams = HospiTeam.objects.all().exclude(accomodation_status='not_req')

    pending_teams = teams.filter(accomodation_status='requested')
    confirmed_teams = teams.filter(accomodation_status='confirmed')
    waitlisted_teams = teams.filter(accomodation_status='waitlisted')
    rejected_teams = teams.filter(accomodation_status='rejected')
    
    num_pending_teams = len(pending_teams)
    num_confirmed_teams = len(confirmed_teams)
    num_waitlisted_teams = len(waitlisted_teams)
    num_rejected_teams = len(rejected_teams)

    num_total_members_pending = 0
    num_male_members_pending = 0
    num_female_members_pending = 0

    num_total_members_confirmed = 0
    num_male_members_confirmed = 0
    num_female_members_confirmed = 0

    num_total_members_waitlisted = 0
    num_male_members_waitlisted = 0
    num_female_members_waitlisted = 0

    num_total_members_rejected = 0
    num_male_members_rejected = 0
    num_female_members_rejected = 0


    for team in pending_teams:
        num_total_members_pending += team.get_total_count()
        num_male_members_pending += team.get_male_count()
        num_female_members_pending += team.get_female_count()

    for team in confirmed_teams:
        num_total_members_confirmed += team.get_total_count()
        num_male_members_confirmed += team.get_male_count()
        num_female_members_confirmed += team.get_female_count()

    for team in waitlisted_teams:
        num_total_members_waitlisted += team.get_total_count()
        num_male_members_waitlisted += team.get_male_count()
        num_female_members_waitlisted += team.get_female_count()

    for team in rejected_teams:
        num_total_members_rejected += team.get_total_count()
        num_male_members_rejected += team.get_male_count()
        num_female_members_rejected += team.get_female_count()

    num_total_members = num_total_members_pending + num_total_members_confirmed + \
        num_total_members_waitlisted + num_total_members_rejected

    num_male_members = num_male_members_pending + num_male_members_confirmed + \
        num_male_members_waitlisted + num_male_members_rejected

    num_female_members = num_female_members_pending + num_female_members_confirmed + \
        num_female_members_waitlisted + num_female_members_rejected

    num_total_teams = num_pending_teams + num_confirmed_teams + \
        num_waitlisted_teams + num_rejected_teams

    html_content = render_to_string('portals/hospi/statistics.html', locals(), RequestContext(request))
    return json.dumps({'html_content':html_content})

@dajaxice_register
def add_hostel_room(request):
    hostelform = HostelForm()
    roomform = RoomForm()
    to_return = {
        'hostelform':hostelform,
        'roomform':roomform,
    }
    html_content = render_to_string('portals/hospi/add_hostel_rooms.html', to_return , RequestContext(request))
    return json.dumps({'html_content':html_content})

@dajaxice_register
def room_map(request):				#By Balaji
    hostels = Hostel.objects.all()
    to_return = {
        'hostels':hostels,
    }
    html_content = render_to_string('portals/hospi/room_map.html', to_return , RequestContext(request))
    return json.dumps({'html_content':html_content})

@dajaxice_register
def add_hostel(request,form_add_hostel):			#By Balaji
    hostelform=HostelForm(deserialize_form(form_add_hostel))
    message = ""
    print "function"
    if hostelform.is_valid():
    	print "valid form"
        hostelform.save()
        message = "Successfully added"
    else:
        message = "Some error occured. Please contact webops"

    return json.dumps({'message':message})

@dajaxice_register
def add_room(request,form_add_room):			#By Balaji
    roomform=RoomForm(deserialize_form(form_add_room))
    message = ""
    if roomform.is_valid():
        roomform.save()
        message = "Successfully added"
    else:
        message = "Some error occured. Please contact webops"

    return json.dumps({'message':message})

@dajaxice_register
def registered_teams(request):
    html_content = render_to_string('portals/hospi/registered_teams.html', {}, RequestContext(request))
    return json.dumps({'html_content':html_content})