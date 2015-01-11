# For rendering templates
from django.template import RequestContext
from django.template.loader import render_to_string
import json
from django.contrib.auth.models import User
from apps.users.forms import UserProfileForm
from apps.hospi.models import HospiTeam, Hostel, Room, Allotment, HospiLog
from apps.hospi.forms import HostelForm, RoomForm, HospiTeamForm
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from django.shortcuts import get_object_or_404
from apps.hospi import utility as u
from django.contrib import messages
from django.conf import settings
from apps.users.models import UserProfile
from post_office import mail
import datetime as dt

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
def hostel_details(request, hostel_id):
    hostel = get_object_or_404(Hostel, pk=hostel_id)
    rooms = hostel.parent_hostel.all()
    to_return={
        'hostel':hostel,
        'rooms':rooms,
    }
    html_content = render_to_string('portals/hospi/hostel_details.html', to_return , RequestContext(request))
    return json.dumps({'html_content':html_content})

@dajaxice_register
def room_details(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    occupants = room.occupants.all()
    to_return={
        'occupants':occupants,
        'room':room,
    }
    html_content = render_to_string('portals/hospi/room_details.html', to_return , RequestContext(request))
    return json.dumps({'html_content':html_content})

@dajaxice_register
def confirm_delete_room(request, room_id):
    room = Room.objects.get(pk=room_id)
    name = room.name
    return json.dumps({'roomname':name, 'room_id':room_id})

@dajaxice_register
def delete_room(request, room_id):
    room = Room.objects.get(pk=room_id)
    message = ""
    if(room):
        room.delete()
        message = "Successfully Deleted"
    else:
        message = "Unable to delete Room. Contact webops team"
    return json.dumps({'message':message})

@dajaxice_register
def confirm_delete_hostel(request, hostel_id):
    hostel = Hostel.objects.get(pk=hostel_id)
    name = hostel.name
    return json.dumps({'hostelname':name, 'hostel_id':hostel_id})

@dajaxice_register
def delete_hostel(request, hostel_id):
    hostel = Hostel.objects.get(pk=hostel_id)
    message = ""
    if(hostel):
        hostel.delete()
        message = "Successfully Deleted"
    else:
        message = "Unable to delete Hostel. Contact webops team"
    return json.dumps({'message':message})

@dajaxice_register
def add_team(request):
    addteamForm = HospiTeamForm()
    to_return={
        'form': addteamForm,
        }
    html_content = render_to_string('portals/hospi/add_team.html', to_return , RequestContext(request))
    return json.dumps({'html_content':html_content})

def auto_id(team_id):
    base = 'SA2015A'
    num = "{0:0>3d}".format(team_id)
    sid = base + num
    return sid

@dajaxice_register
def adding_team(request,form_add_team, user_id):
    teamform = deserialize_form(form_add_team)
    new_team = HospiTeam()
    print teamform['name']
    print teamform['city']
    print teamform['accomodation_status']

    message = ""
    user = User.objects.get(pk=int(user_id))
    new_team.leader  = user.profile
    #new_team.leader = get_object_or_404(UserProfile, pk=user_id)
    new_team.name = teamform['name']
    new_team.accomodation_status = teamform['accomodation_status']
    new_team.city = teamform['city']
    new_team.date_of_arrival = teamform['date_of_arrival']
    new_team.time_of_arrival = teamform['time_of_arrival']
    new_team.date_of_departure = teamform['date_of_departure']
    new_team.time_of_departure = teamform['time_of_departure']
    new_team.team_sid = 'SA2015A'
    new_team.save()
    new_team.team_sid = auto_id(new_team.id)
    new_team.save()
    # if teamform.is_valid():
    #     teamform.leader = user_id

    #     team = teamform.save()
    #     #team.leader = user_id
    #     team.save()
    #     message = "Successfully added"
    # else:
    message='Successfully added team. Please wait till page refreshes automatically'
    #     for i in teamform.errors:
    #         message+=i
        #message = teamform.errors  #"Some error occured. Please fill the form again. If problem persists, contact webops Team."

    return json.dumps({'message':message})

@dajaxice_register
def team_details(request, team_id):
    team = get_object_or_404(HospiTeam, pk=team_id)
    edit_list = ['confirmed', 'rejected']
    leader = team.leader
    bill_data = u.bill(team.date_of_arrival, team.time_of_arrival, team.date_of_departure, team.time_of_departure, team.get_total_count())
    if team.accomodation_status in edit_list:
        editable = False
    else:
        editable=True
    to_return = {
        'leader':leader,
        'bill_data':bill_data,
        'addUserForm':UserProfileForm(),
        'editable':editable,
        'team':team,
    }
    html_content = render_to_string('portals/hospi/team_details.html', to_return , RequestContext(request))
    return json.dumps({'html_content':html_content})

@dajaxice_register
def update_status(request, stat, team_id):
    team = get_object_or_404(HospiTeam, pk=team_id)
    if team.members.filter(email=team.leader.email):
        team.members.remove(team.leader)
        messages.warning(request, 'For '+ team.name + ' : ' + team.team_sid +', Team leader found in members list also. Successfully removed!')
    if stat:
        if stat == 'confirmed':
            team.leader.accomod_is_confirmed = True
            team.leader.save()
            for member in team.members.all():
                if member.accomod_is_confirmed == False:
                    member.accomod_is_confirmed = True
                    member.save()
                else:
                    team.members.remove(member)
            team.save()
            a=Allotment.objects.create(team=team, alloted_by=request.user)
            a.save()
        team.accomodation_status = stat
        team.save()
        messages.success(request, 'Status for '+team.name+' successfully updated to '+stat)
        emailsubject='Accommodation request '+stat+', Saarang 2015'
        users=[]
        for user in team.get_all_members():
            users.append(user.user.email)
        if stat == 'confirmed':
            mail.send(
                users, template='confirm_accommodation.email',
                context={'team':team,}
                )

            unsubscribe_link = "dasdasdasei8rwer9f898fasd89a"
            mail.send(
                sender = settings.DEFAULT_MAIN_FROM_EMAIL,
                recipients = users,
                template = 'hospitality_payment.email',
                context = {'FEST_NAME': settings.FEST_NAME, 'SITE_URL': settings.SITE_URL, 'unsubscribe_link': unsubscribe_link},
                headers = {'List-Unsubscribe': unsubscribe_link}
            ) 
        else:
            mail.send(
                users, template='status_update.email',
                context={'status':stat, 'team':team,}
                )
		
    return json.dumps({'stat':stat})

@dajaxice_register
def check_in(request, team_id):
    '''Needs to add some validators'''
    team = get_object_or_404(HospiTeam, pk=team_id)
    if team.get_male_count() == 0 and team.get_female_count==0:
        messages.error(request, 'Incomplete team profile')
    if team.members.filter(email=team.leader.email):
        team.members.remove(team.leader)
    if team.get_female_count() and team.get_male_count():
        #print 'Mixed Team'
        html_content = "<div class='alert alert-danger'>Split Team Before Check-in</div>"
        return json.dumps({'html_content':html_content})
    elif team.get_male_count():
        #print 'Male Team'
        males = team.get_male_members()
        male_rooms = Room.objects.filter(hostel__gender='male')
        html_content = render_to_string('portals/hospi/check_in_males.html', locals(), RequestContext(request))
        return json.dumps({'html_content':html_content})
    elif team.get_female_count():
        #print 'Female Team'
        females = team.get_female_members()
        female_rooms = Room.objects.filter(hostel__gender='female')
        html_content = render_to_string('portals/hospi/check_in_females.html', locals(), RequestContext(request))
        return json.dumps({'html_content':html_content})
    else:
        html_content = "<div class='alert alert-danger'>Incomplete team profile</div>"
        return json.dumps({'html_content':html_content})

@dajaxice_register
def del_member(request, team_id, member_id):
    user = get_object_or_404(UserProfile, pk=member_id)
    message = "Do you want to remove " + str(user.user.get_full_name()) + " ?"
    return json.dumps({'message':message, 'team_id':team_id, 'member_id':member_id})

@dajaxice_register
def delete_member(request, team_id, member_id):
    team = HospiTeam.objects.get(pk=team_id)
    data = request.POST.copy()
    user = get_object_or_404(UserProfile, pk=member_id)
    message = "Successfully removed " + str(user.user.get_full_name())
    team.members.remove(user)
    user.save()
    team.save()
    return json.dumps({'message':message})

@dajaxice_register
def del_member_from_room(request, room_id, user_id):
    try:
        room = Room.objects.get(pk=room_id)
        user = get_object_or_404(UserProfile, pk=user_id)
        room.occupants.remove(user)
        room.save()
        message = "Success"
    except:
        message = "Error"
    return json.dumps({'message':message, 'room_id':room_id})

@dajaxice_register
def add_member_to_room(request, room_id, user_id):
    try:
        room = Room.objects.get(pk=room_id)
        user = get_object_or_404(User, pk=user_id)
        room.occupants.add(user.profile)
        room.save()
        message = "Success"
    except Exception, e:
        message = "Error"+e.message
    return json.dumps({'message':message, 'room_id':room_id})


def days(in_date, in_time, out_date, out_time):
    l1 = dt.datetime(2015, 1, 7, 10, 0)
    u1 = dt.datetime(2015, 1, 8, 17, 0)
    l2 = dt.datetime(2015, 1, 8, 5, 0)
    u2 = dt.datetime(2015, 1, 9, 17, 0)
    l3 = dt.datetime(2015, 1, 9, 5, 0)
    u3 = dt.datetime(2015, 1, 10, 17, 0)
    l4 = dt.datetime(2015, 1, 10, 5, 0)
    u4 = dt.datetime(2015, 1, 11, 17, 0)
    l5 = dt.datetime(2015, 1, 11, 5, 0)
    u5 = dt.datetime(2015, 1, 12, 9, 0)
    
    span = [[l1,u1],[l2,u2],[l3,u3],[l4,u4],[l5,u5]]

    in_stamp = dt.datetime.combine(in_date, in_time)
    out_stamp = dt.datetime.combine(out_date, out_time)

    for i in xrange(0,5):
        if (in_stamp >= span[i][0] and in_stamp <= span[i][1] and in_stamp<span[i+1][0] ):
            for j in xrange(i,5):
                if out_stamp >= span[j][0] and out_stamp <= span[j][1]:
                    return j-i+1
    return 0

@dajaxice_register
def ohm(request):
    teams = HospiTeam.objects.all()
    data = []
    for team in teams:
        dos = days(team.date_of_arrival,team.time_of_arrival,team.date_of_departure,team.time_of_departure)
        ohm = team.get_total_count()*dos*50
        data.append({'team':team, 'ohm':ohm, 'dos':dos})
    to_return = {
        'data':data,
    }
    html_content = render_to_string('portals/hospi/ohm.html', to_return, RequestContext(request))
    return json.dumps({'html_content':html_content})
