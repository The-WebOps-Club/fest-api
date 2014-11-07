# For rendering templates
from django.template import RequestContext
from django.template.loader import render_to_string
import json
from apps.hospi.models import HospiTeam, Hostel, Room, Allotment, HospiLog
from dajaxice.decorators import dajaxice_register

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
def registered_teams(request):
    html_content = render_to_string('portals/hospi/registered_teams.html', {}, RequestContext(request))
    return json.dumps({'html_content':html_content})