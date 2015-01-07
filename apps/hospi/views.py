# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail, send_mass_mail, EmailMessage
import utility as u
import random, string, json
from random import *
from models import Hostel, Room, HospiTeam, Allotment, HospiLog
from apps.events.models import Team, EventRegistration, Event
from django.contrib.auth.models import User
from forms import HostelForm, RoomForm, HospiTeamForm, UserProfileForm
#from apps.events.forms import AddTeamForm
from post_office import mail
import datetime
from django.views.decorators.csrf import csrf_exempt
from apps.users.models import UserProfile, Team
from apps.events.models import EventRegistration
from django.views.decorators.cache import never_cache
####################################################################
# Mainsite Views

@never_cache
def prehome(request):
    if not request.user.is_authenticated():
        return render(request, 'portals/hospi/login.html', locals())

    user = request.user.profile
    #events teams
    # teams_leading = user.team_leader.all().exclude(accomodation_status='hospi')
    # teams_member = user.team_members.all()
    teams_leading = []
    teams_member = []
    events_leading = EventRegistration.objects.filter(users_registered=user.user, teams_registered__isnull=False)
    events_members = user.user.teams
    for event in events_leading:
        teams_leading.append(event.teams_registered)
    for team in events_members.all():
        if team not in teams_leading:
            teams_member.append(team)
    hospi_teams_leading = user.hospi_team_leader.all()
    hospi_teams_member = user.hospi_team_members.all()
    if not user.profile_is_complete():
        messages.error(request, "Your profile is not complete. Click on your name on upper right corner to update your profile. ")
    return render(request, 'portals/hospi/prehome.html', locals())

def set_hospi_team(request, team_id):
    team = get_object_or_404(HospiTeam, pk=team_id)
    members = team.members.all()
    confirmed_list=[]
    if team.leader.accomod_is_confirmed:
        messages.error(request, 'Your accommodation has been confirmed in another team. \
            You cannot request for accommodation again.')
        return redirect('hospi_prehome')

    team.accomodation_status = 'requested'
    team.save()
    request.session['current_team'] = team_id
    return redirect('hospi_home', team_id=team_id)

def set_event_team(request, event_team_id):
    user=request.user.profile
    event_team = get_object_or_404(Team, pk=event_team_id)
    if user.accomod_is_confirmed:
        messages.error(request, 'Your accommodation has been confirmed in another team. \
            You cannot request for accommodation again.')
        return redirect('hospi_prehome')
    team = HospiTeam.objects.create(name=event_team.name, \
        leader=user, accomodation_status='requested',\
        city=user.city)
    for user2 in event_team.members.all():
        team.members.add(user2.profile)
    team.team_sid = auto_id(team.pk)
    event_team.accomodation_status = 'hospi'
    event_team.save()
    team.save()
    request.session['current_team'] = team.pk
    return redirect('hospi_home', team_id=team.pk)

def details(request, team_id):
    team = get_object_or_404(HospiTeam, pk=team_id)
    request.session['current_team'] = team.pk
    return redirect('hospi_home', team_id=team.pk)
    
@never_cache
def home(request, team_id):
    user = request.user.profile
    if not user.profile_is_complete():
        messages.warning(request, "Your profile is not complete. Click on your name on upper right corner to update your profile. ")
        return redirect('hospi_prehome')
    team = get_object_or_404(HospiTeam, pk=team_id)
    if not team.city:
        team.city = user.city
        team.save()
    if team.members.filter(saarang_id=team.leader.saarang_id):
        team.members.remove(team.leader)
        messages.warning(request, 'Team leader found in members list also. Successfully removed!')
    members = team.members.all()
    msg=''
    if team.accomodation_status != 'confirmed':
        for member in members:
            if member.accomod_is_confirmed:
                msg += str(member.email) +', '
        if msg:
            messages.warning(request, msg + ': These members already have accommodation \
                confirmed in other team. Please remove them, or they will be automatically \
                removed upon confirmation.')
    edits = ['not_req', 'requested']
    if team.accomodation_status in edits:
        editable = True
    else:
        editable = False
    bill_data = u.bill(team.date_of_arrival, team.time_of_arrival, team.date_of_departure, team.time_of_departure, team.get_total_count())
    to_return = {
        'editable':editable,
        'leader':user,
        'team':team,
        'members':members,
        'bill_data':bill_data,
    }
    return render(request, 'portals/hospi/home.html', to_return)

def login(request):
    if request.method == 'POST':
        data=request.POST.copy()
        try:
            user = SaarangUser.objects.get(email=data['email'])
            try:
                teams = user.team_leader.all()
            except Exception, e:
                messages.error(request, 'You do not lead any team. Please create a team.')
                return render(request, 'hospi/login.html')
            if user.password == data['password']:
                request.session['saaranguser_email'] = user.email
                return redirect('hospi_prehome')
            else:
                messages.error(request, 'Did you misspell your password?')
        except Exception, e:
            messages.error(request, 'Is your email id correct?')
    return render(request, 'hospi/login.html')

def logout(request):
    try:
        del request.session['saaranguser_email']
        messages.success(request, 'You have been logged out.')
    except KeyError:
        messages.warning(request, 'Please login first.')
    return redirect('hospi_login')


def add_members(request):
    data = request.POST.copy()
    team = get_object_or_404(HospiTeam, pk=data['team_id'])
    return_list = dict(request.POST)['saarang_id']
    not_registered =[]
    members = []
    profile_not_complete=[]
    added=[]
    print return_list
    for member in return_list:
        print member
        members.append(member)
        try:
            user = UserProfile.objects.get(saarang_id=member)
            if user.profile_is_complete():
                new = team.members.add(user)
                added.append(user.user.email)
            else:
                profile_not_complete.append(user.user.email)
        except Exception, e:
            not_registered.append(member)
    if added:
        t=''
        for email in added:
            t+=email+', '
        messages.success(request, "Successfully added "+t)
        mail.send(
            added, template='hospi_leader_added_member.email',
            context={'team':team,},
            )

    if not_registered:
        msg=''
        for email in not_registered:
            msg += email + ', '
        messages.error(request,'Partially added /could not add members. ' + msg + 'have not registered \
                with Saarang yet. Please ask them to register and try adding them again.')

    if profile_not_complete:
        print profile_not_complete
        txt = ''
        for email in profile_not_complete:
            txt += email + ', '
        messages.warning(request, 'Profile not complete. '+txt+" have not completed their profile at Saarang. Please ask them to click on the link they recieved thru email to update their profile, or ask them to update profile. ")
        mail.send(
            profile_not_complete, template='hospi_profile_incomplete.email',
            context={'team':team,}
            )
    return redirect('hospi_home', team_id=team.pk)

def delete_member(request, team_id, member_id):
    team = get_object_or_404(HospiTeam, pk=team_id)
    user = get_object_or_404(UserProfile, pk=member_id)

    team.members.remove(user)
    return redirect('hospi_home', team_id=team.pk)

def add_accomodation(request):
    data = request.POST.copy()
    team = get_object_or_404(HospiTeam, pk=data['team_id'])
    if data['updating'] == 'all':
        team.date_of_arrival = data['arr_date']
        team.date_of_departure = data['dep_date']
        team.time_of_arrival = data['arr_time']
        team.time_of_departure = data['dep_time']
        if team.accomodation_status == 'not_req':
            team.accomodation_status = 'requested'
            messages.success(request, 'Successfully requested for accommodation.')
        else:
            messages.success(request, 'Details successfully updated.')
        team.save()
        return redirect('hospi_home',team_id=team.pk)
    elif data['updating'] == 'control_room':
        team.date_of_arrival = data['arr_date']
        team.date_of_departure = data['dep_date']
        team.time_of_arrival = data['arr_time']
        team.time_of_departure = data['dep_time']
        team.save()
        messages.success(request, 'Saved successfully')
        return redirect('hospi_team_details', int(data['team_id']))
    return redirect('hospi_home', team_id=team.pk)


def user_add_team(request):
    addteamForm = HospiTeamForm()
    to_return={
        'form': addteamForm,
        }
    return render(request, 'hospi/add_team.html', to_return)

def user_save_team(request):
    data = request.POST.copy()
    user = request.user.profile
    if not data['team_name']:
        data['team_name'] = user.user.first_name + " Team"
    try:
        team = HospiTeam.objects.create(name=data['team_name'], leader=user, city=user.city )
        team.team_sid = auto_id(team.pk)
        team.save()
        messages.success(request, team.name +' added successfully. Saarang ID is '+team.team_sid)
    except Exception, e:
        messages.error(request, 'Some random error occured. please try again: ' + e.message)
    return redirect('hospi_prehome')

def cancel_request(request, team_id):
    user = request.user.profile
    team = get_object_or_404(HospiTeam, pk=team_id)
    members = team.get_all_members()
    if team.accomodation_status == 'confirmed':
        for member in members:
            member.accomod_is_confirmed = False
            member.save()
    team.accomodation_status = 'not_req'
    team.save()
    messages.success(request, 'Accommodation request cancelled successfully!')
    return redirect('hospi_prehome')

def delete_team(request, team_id):
    user = request.user.profile
    team = get_object_or_404(HospiTeam, pk=team_id)
    team.delete()
    messages.success(request, 'Team has been successfully deleted')
    return redirect('hospi_prehome')

def generate_saar(request, team_id):
    user = request.user.profile
    team = get_object_or_404(HospiTeam, pk=team_id)
    leader = team.leader
    if team.leader != user:
        messages.error(request, 'Please login first')
        return redirect('hospi_login')
    members = team.members.all()
    # return render(request, 'hospi/saar.html', locals())
    return u.generate_pdf(request, team_id)

# End Mainsite views
#######################################################################

# ERP views

@login_required
def list_registered_teams(request):
    dept_list= ['hospi', 'webops']
    if not request.user.userprofile.dept.name in dept_list:
        return render(request, 'alert.html', {'msg':'You dont have permission',})
    teams = HospiTeam.objects.all().exclude(accomodation_status='not_req')
    to_return = {
       'teams':teams,
    }
    return render(request, 'hospi/registered_teams.html', to_return)

@login_required
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
    return render(request, 'portals/hospi/team_details.html', to_return)

@login_required
def print_saar(request, team_id):
    return u.generate_pdf(request, team_id)

def split_team(request, team_id):
    team = get_object_or_404(HospiTeam, pk=team_id)
    M=['male', 'Male', 'm','M']
    F=['female', 'Female','f','F']
    if team.leader.gender in M:
        female_members = team.get_female_members()
        team_leader = female_members.pop(0)
        new_team = HospiTeam.objects.create(name=team.name+'_Female', leader=team_leader)
        new_team.team_sid = auto_id(new_team.pk)
        for member in female_members:
            new_team.members.add(member)
            team.members.remove(member)
        team.members.remove(team_leader)
        team.save()
        new_team.accomodation_status = team.accomodation_status
        new_team.city = team.city
        new_team.date_of_arrival = team.date_of_arrival
        new_team.time_of_arrival = team.time_of_arrival
        new_team.date_of_departure = team.date_of_departure
        new_team.time_of_departure = team.time_of_departure
        new_team.save()
    elif team.leader.gender in F:
        male_members = team.get_male_members()
        team_leader = male_members.pop(0)
        new_team = HospiTeam.objects.create(name=team.name+'_Male', leader=team_leader)
        new_team.team_sid = auto_id(new_team.pk)
        for member in male_members:
            new_team.members.add(member)
            team.members.remove(member)
        team.members.remove(team_leader)
        team.save()
        new_team.accomodation_status = team.accomodation_status
        new_team.city = team.city
        new_team.date_of_arrival = team.date_of_arrival
        new_team.time_of_arrival = team.time_of_arrival
        new_team.date_of_departure = team.date_of_departure
        new_team.time_of_departure = team.time_of_departure
        new_team.save()
    messages.success(request, 'Team '+new_team.name+' created and ID is '+new_team.team_sid)
    return redirect('hospi_team_details', team.pk)

@login_required
def update_status(request, team_id):
    team = get_object_or_404(HospiTeam, pk=team_id)
    if team.members.filter(email=team.leader.email):
        team.members.remove(team.leader)
        messages.warning(request, 'For '+ team.name + ' : ' + team.team_sid +', Team leader found in members list also. Successfully removed!')
    data = request.POST.copy()
    stat = ''
    try:
        stat=data['status']
    except Exception, e:
        pass
    if stat:
        print stat
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
            users.append(user.email)
        if stat == 'confirmed':
            mail.send(
                users, template='email/hospi/confirm_accommodation',
                context={'team':team,}
                )
        else:
            mail.send(
                users, template='email/hospi/status_update',
                context={'status':stat, 'team':team,}
                )
    return redirect('hospi_list_registered_teams')

@login_required
def statistics(request):
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

    return render(request, 'hospi/statistics.html', locals())

#####################################################################################

# Hospi Control room
@login_required
def add_hostel_rooms(request):
    hostelform = HostelForm()
    roomform = RoomForm()
    to_return = {
        'hostelform':hostelform,
        'roomform':roomform,
    }
    return render(request, 'hospi/add_hostel_rooms.html', to_return)

@login_required
def add_hostel(request):
    try:
        hostel = HostelForm(request.POST)
        hos = hostel.save()
        messages.success(request, 'Hostel ' + hos.name + ' successfully added')
    except Exception, e:
        messages.error(request, 'Some error occured. Please contact webops with this message: '+ e.message)
    return redirect('hospi_room_map')

@login_required
def add_room(request):
    try:
        room = RoomForm(request.POST)
        rom = room.save()
        messages.success(request, 'Room ' + rom.name + ' successfully added')
    except Exception, e:
        messages.error(request, 'Some error occured. Please contact webops with this message: '+ e.message)
    return redirect('hospi_room_map')

@login_required
def room_map(request):
    hostels = Hostel.objects.all()
    to_return = {
        'hostels':hostels,
    }
    return render(request, 'hospi/room_map.html', to_return)

@login_required
def hostel_details(request, hostel_id):
    hostel = get_object_or_404(Hostel, pk=hostel_id)
    rooms = hostel.parent_hostel.all()
    to_return={
        'hostel':hostel,
        'rooms':rooms,
    }
    return render(request, 'hospi/hostel_details.html', to_return)

@login_required
def room_details(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    occupants = room.occupants.all()
    to_return={
        'occupants':occupants,
        'room':room,
    }
    return render(request, 'hospi/room_details.html', to_return)

@login_required
def list_all_teams(request):
    dept_list= ['hospi', 'webops']
    if not request.user.userprofile.dept.name in dept_list:
        return render(request, 'alert.html', {'msg':'You dont have permission',})
    teams = HospiTeam.objects.all()
    to_return={
        'teams':teams,
    }
    return render(request, 'hospi/list_all_teams.html', to_return)    

def auto_id(team_id):
    base = 'SA2015A'
    num = "{0:0>3d}".format(team_id)
    sid = base + num
    return sid

@login_required
def add_team(request):
    addteamForm = HospiTeamForm()
    to_return={
        'form': addteamForm,
        }
    return render(request, 'hospi/add_team.html', to_return)

@login_required
def save_team(request):
    addteamForm = HospiTeamForm(request.POST)
    data = request.POST.copy()
    if addteamForm.is_valid():
        try:
            team = addteamForm.save()
            team.team_sid = auto_id(team.pk)
            team.save()
            messages.success(request, team.name +' added successfully. Saarang ID is '+team.team_sid)
        except Exception, e:
            messages.error(request, 'Some error occured. please try again: ' + e.message)
    else:
        messages.error(request, 'Some error occured. please try again')
    return redirect('hospi_list_registered_teams')

@login_required
def check_in_team(request, team_id):
    '''Needs to add some validators'''
    team = get_object_or_404(HospiTeam, pk=team_id)
    if team.get_male_count() == 0 and team.get_female_count==0:
        messages.error(request, 'Incomplete team profile')
    if team.members.filter(email=team.leader.email):
        team.members.remove(team.leader)
    if team.get_female_count() and team.get_male_count():
        print 'Mixed Team'
        males = team.get_male_members()
        females = team.get_female_members()
        male_rooms = Room.objects.filter(hostel__gender='male')
        female_rooms = Room.objects.filter(hostel__gender='female')
        return render(request, 'hospi/check_in_mixed.html', locals())
    elif team.get_male_count():
        print 'Male Team'
        males = team.get_male_members()
        male_rooms = Room.objects.filter(hostel__gender='male')
        return render(request, 'hospi/check_in_males.html', locals())
    elif team.get_female_count():
        print 'Female Team'
        females = team.get_female_members()
        female_rooms = Room.objects.filter(hostel__gender='female')
        return render(request, 'hospi/check_in_females.html', locals())
    return HttpResponse("<div class='alert alert-error'> Incomplete team profile</div>")

@login_required
def check_in_mixed(request):
    data = request.POST.copy()
    team = get_object_or_404(HospiTeam, pk=data['team_id'])
    males = team.get_male_members()
    females = team.get_female_members()
    for male in males:
        room = get_object_or_404(Room, pk=data[male.saarang_id])
        room.occupants.add(male)
        room.save()
        HospiLog.objects.create(created_by=request.user, user=male, room=room)
    for female in females:
        room = get_object_or_404(Room, pk=data[female.saarang_id])
        room.occupants.add(female)
        room.save()
        HospiLog.objects.create(created_by=request.user, user=female, room=room)
    team.mattress_count=data['matress']
    team.checked_in = True
    team.save()
    messages.success(request, team.team_sid + ' checked in successfully')
    return redirect('hospi_list_registered_teams')

def check_in_males(request):
    room_history = ""
    data = request.POST.copy()
    team = get_object_or_404(HospiTeam, pk=data['team_id'])
    males = team.get_male_members()
    for male in males:
        room = get_object_or_404(Room, pk=data[male.saarang_id])
        room.occupants.add(male)
        room.save()
        room_history += room.hostel.name + '(' + room.name +')\n' 
    team.checked_in = True
    team.room_history = room_history
    team.mattress_count=data['matress']
    team.save()
    messages.success(request, team.team_sid + ' checked in successfully')
    return redirect('hospi_team_details', team.pk)

def check_in_females(request):
    room_history = ""
    data = request.POST.copy()
    team = get_object_or_404(HospiTeam, pk=data['team_id'])
    females = team.get_female_members()
    for female in females:
        room = get_object_or_404(Room, pk=data[female.saarang_id])
        room.occupants.add(female)
        room.save()
        room_history += room.hostel.name + '(' + room.name +')\n' 
    team.checked_in = True
    team.room_history = room_history
    team.mattress_count=data['matress']
    team.save()
    messages.success(request, team.team_sid + ' checked in successfully')
    return redirect('hospi_team_details', team.pk)

def check_out_team(request, team_id):
    team = get_object_or_404(HospiTeam, pk=team_id)
    members = team.get_all_members()
    for member in members:
        rooms = member.room_occupant.all()
        for room in rooms:
            room.occupants.remove(member)
            room.save()
                 
    team.checked_out = True
    team.save()
    messages.success(request, team.team_sid + ' checked out successfully')
    return u.checkout_bill(request,team_id)
    #try:
    #    room = team.leader.room_occupant.all()[0]
    #    room.occupants.remove(team.leader)
    #    room.save()
    #    log_entry = HospiLog.objects.get(user=team.leader)
    #    log_entry.checked_out = True
    #    log_entry.checkout_time = datetime.datetime.now()
    #    log_entry.checked_out_by = request.user
    #    log_entry.save()
    #except:
    #    return u.checkout_bill(request, team_id)
    #for member in members:
    #    try:
    #        room = member.room_occupant.all()[0]
    #        room.occupants.remove(member)
    #        room.save()
    #        log_entry = HospiLog.objects.get(user=member)
    #        log_entry.checked_out = True
    #        print log_entry
    #        log_entry.checkout_time = datetime.datetime.now()
    #        log_entry.checked_out_by = request.user
    #        log_entry.save()
    #    except Exception, e:
    #        return u.checkout_bill(request, team_id)
    #return redirect('hospi_team_details', team.pk)

def print_bill(request, team_id):
    return u.checkout_bill(request, team_id)
    
@csrf_exempt
@login_required
def update_member(request):
    data = request.POST.copy()
    user = get_object_or_404(UserProfile, pk=int(data['id']))
    if '.' in data['columnName'] and data['columnName'].split('.')[0] == 'user':
        user = user.user
        print data['columnName'], data['value']
        setattr(user, data['columnName'].split('.')[1], data['value'])
    else:
        setattr(user, data['columnName'], data['value'])
    user.save()
    print user
    return HttpResponse(data['value'])

def add_member(request,team_id):
    team = HospiTeam.objects.get(pk=team_id)
    if request.method == 'POST':
        form =UserProfileForm(request.POST)
        print request.POST
        try:
            if form.is_valid():
                user = User()
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.email = form.cleaned_data['email']
                user.username = user.email
                characters = string.ascii_letters + string.punctuation  + string.digits
                password =  "".join(choice(characters) for x in range(randint(8, 16)))
                user.password = password
                user.save()
                userp = UserProfile()
                userp.user = user
                userp.age = form.cleaned_data['age']
                userp.gender = form.cleaned_data['gender']
                userp.mobile_number = form.cleaned_data['mobile_number']
                userp.branch = form.cleaned_data['branch']
                userp.college_text = form.cleaned_data['college_text']
                userp.college_roll = form.cleaned_data['college_roll']
                userp.save()
                team.members.add(userp)
                team.save()
                '''mail.send(
                    [user.email], template='email/main/activate_confirm',
                    context={'saarang_id':user.saarang_id, 'password':user.password}
                )'''
                messages.success(request, 'User added successfully')
            else:
                print "Invalid"
        except Exception, e:
            return HttpResponse("User is already registered on Saarang Website. Use Add existing user, and search by email")
    return redirect('hospi_team_details', team.pk)

@csrf_exempt
@login_required
def del_member(request, team_id, member_id):
    team = HospiTeam.objects.get(pk=team_id)
    data = request.POST.copy()
    user = get_object_or_404(UserProfile, pk=member_id)
    team.members.remove(user)
    user.save()
    team.save()
    return redirect('hospi_team_details', team.pk)

def id_search(request):
    data=request.GET.copy()
    user_list = []
    selected_users=[]
    users_id = UserProfile.objects.filter(saarang_id=data['q'].upper())
    users_email = UserProfile.objects.filter(user__email__icontains=data['q'])[:10]
    for user in users_id:
        selected_users=selected_users+[user]
    for user in users_email:
        selected_users=selected_users+[user]
    selected_users=list(set(selected_users))

    for user in selected_users:
        user_list.append({"desk_id":user.desk_id,'id':user.user.id,'saarang_id':user.saarang_id, 'email':user.user.email, 'first_name':user.user.first_name,'last_name':user.user.last_name, 'mobile_number':user.mobile_number, 'city':user.city,  'branch':user.branch, 'college_text':user.college_text, 'age':user.age, 'want_accomodation':user.want_accomodation, 'gender':user.gender.capitalize() })
    user_dict = json.dumps(user_list)
    return HttpResponse(user_dict)

@login_required
def add_user_to_team(request):
    data = request.POST.copy()
    try:
        print int(data['team_id'])
        print int(data['website_id'])
        team = get_object_or_404(HospiTeam, pk=int(data['team_id']))
        user = get_object_or_404(User, pk=int(data['website_id']))
        team.members.add(user.profile)
        team.save()
        messages.success(request, 'User added successfully')
    except:
        messages.error(request, 'Error, please try again!!')
    return redirect('hospi_team_details', int(data['team_id']))

@login_required
def delete_room(request, room_id):
    room = Room.objects.get(pk=room_id)
    return HttpResponse('Under construction')



