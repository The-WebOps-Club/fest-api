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
from registration.views import auto_id as uid
from registration.models import SaarangUser
from registration.forms import SaarangUserForm
from models import Hostel, Room, HospiTeam, Allotment, HospiLog
from events.models import Team, EventRegistration, Event
from forms import HostelForm, RoomForm, HospiTeamForm
from events.forms import AddTeamForm
from mailer.models import MailLog
from post_office import mail
import datetime
from django.views.decorators.csrf import csrf_exempt

####################################################################
# Mainsite Views

def prehome(request):
    if not request.session.get('saaranguser_email'):
        return redirect('hospi_login')
    email = request.session.get('saaranguser_email')
    user = SaarangUser.objects.get(email=email)
    teams_leading = user.team_leader.all().exclude(accomodation_status='hospi')
    teams_member = user.team_members.all()
    hospi_teams_leading = user.hospi_team_leader.all()
    hospi_teams_member = user.hospi_team_members.all()
    if not user.profile_is_complete():
        messages.error(request, "Your profile is not complete. Click <a href='http://saarang.org/2014/main/#profile' target='_blank'>here</a> to update your profile. ")
    return render(request, 'hospi/prehome.html', locals())

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
    return redirect('hospi_home')

def set_event_team(request, event_team_id):
    event_team = get_object_or_404(Team, pk=event_team_id)
    if event_team.leader.accomod_is_confirmed:
        messages.error(request, 'Your accommodation has been confirmed in another team. \
            You cannot request for accommodation again.')
        return redirect('hospi_prehome')
    team = HospiTeam.objects.create(name=event_team.name, \
        leader=event_team.leader, accomodation_status='requested')
    for user in event_team.members.all():
        team.members.add(user)
    team.team_sid = auto_id(team.pk)
    event_team.accomodation_status = 'hospi'
    event_team.save()
    team.save()
    request.session['current_team'] = team.pk
    return redirect('hospi_home')

def details(request, team_id):
    team = get_object_or_404(HospiTeam, pk=team_id)
    request.session['current_team'] = team.pk
    return redirect('hospi_home')
    
def home(request):
    if not request.session.get('saaranguser_email'):
        return redirect('hospi_login')
    email = request.session.get('saaranguser_email')
    user = SaarangUser.objects.get(email=email)
    if not user.profile_is_complete():
        messages.error(request, "Your profile is not complete. Click <a href='http://saarang.org/2014/main/#profile' target='_blank'>here</a> to update your profile. ")
        return redirect('hospi_prehome')
    if not request.session.get('current_team'):
        return redirect('hospi_prehome')
    team_id = request.session.get('current_team')
    team = get_object_or_404(HospiTeam, pk=team_id)
    if team.members.filter(email=team.leader.email):
        team.members.remove(team.leader)
        messages.warning(request, 'Team leader found in members list also. Successfully removed!')
    members = team.members.all()
    msg=''
    if team.accomodation_status != 'confirmed':
        for member in members:
            if member.accomod_is_confirmed:
                msg += member.email +', '
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
    return render(request, 'hospi/home.html', to_return)

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
    return_list = zip(dict(request.POST)['email'],dict(request.POST)['college_id'])
    not_registered =[]
    members = []
    profile_not_complete=[]
    added=[]
    for member in return_list:
        uemail = member[0]
        uid = member[1]
        members.append(uemail)
        try:
            user = SaarangUser.objects.get(email=uemail)
            if uid:
                user.college_id = uid
                user.save()
            if user.profile_is_complete():
                new = team.members.add(user)
                added.append(uemail)
            else:
                profile_not_complete.append(uemail)
        except Exception, e:
            not_registered.append(uemail)
    if added:
        t=''
        for email in added:
            t+=email+', '
        messages.success(request, "Successfully added "+t)
        mail.send(
            added, template='email/hospi/leader_added_member',
            context={'team':team,},
            )

    if not_registered:
        msg=''
        for email in not_registered:
            msg += email + ', '
        messages.error(request,'Partially added /could not add members. ' + msg + 'have not registered \
                with Saarang yet. Please ask them to register and try adding them again.')
        mail.send(
            not_registered, template='email/hospi/register_invitation',
            context={'team':team,}
            )

    if profile_not_complete:
        print profile_not_complete
        txt = ''
        for email in profile_not_complete:
            txt += email + ', '
        messages.warning(request, 'Profile not complete. '+txt+" have not completed their profile at Saarang. Please ask them to click on the link they recieved thru email to update their profile, or ask them to Click <a href='http://saarang.org/2014/main/#login' target='_blank'>here</a> to update profile. ")
        mail.send(
            profile_not_complete, template='email/hospi/profile_incomplete',
            context={'team':team,}
            )
    return redirect('hospi_home')

def delete_member(request, team_id, member_id):
    team = get_object_or_404(HospiTeam, pk=team_id)
    user = get_object_or_404(SaarangUser, pk=member_id)

    team.members.remove(user)
    mail.send(
        [user.email], template='email/hospi/member_deleted',
        context={'team':team,}
        )
    return redirect('hospi_home')

def add_accomodation(request):
    data = request.POST.copy()
    team = get_object_or_404(HospiTeam, pk=data['team_id'])
    if data['updating'] == 'city':
        team.city = data['city']
        team.save()
        messages.success(request, 'City updated.')
        return redirect('hospi_home')
    elif data['updating'] == 'all':
        team.city = data['city']
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
        return redirect('hospi_home')
    elif data['updating'] == 'control_room':
        team.date_of_arrival = data['arr_date']
        team.date_of_departure = data['dep_date']
        team.time_of_arrival = data['arr_time']
        team.time_of_departure = data['dep_time']
        team.city = data['city']
        team.save()
        messages.success(request, 'Saved successfully')
        return redirect('hospi_team_details', int(data['team_id']))
    return redirect('hospi_home')


def user_add_team(request):
    addteamForm = HospiTeamForm()
    to_return={
        'form': addteamForm,
        }
    return render(request, 'hospi/add_team.html', to_return)

def user_save_team(request):
    data = request.POST.copy()
    user = SaarangUser.objects.get(email=request.session.get('saaranguser_email'))
    try:
        team = HospiTeam.objects.create(name=data['team_name'], leader=user )
        team.team_sid = auto_id(team.pk)
        team.save()
        messages.success(request, team.name +' added successfully. Saarang ID is '+team.team_sid)
    except Exception, e:
        messages.error(request, 'Some random error occured. please try again: ' + e.message)
    return redirect('hospi_prehome')

def cancel_request(request):
    if not request.session.get('saaranguser_email'):
        return redirect('hospi_login')
    email = request.session.get('saaranguser_email')
    user = SaarangUser.objects.get(email=email)
    if not request.session.get('current_team'):
        return redirect('hospi_prehome')
    team_id = request.session.get('current_team')
    team = get_object_or_404(HospiTeam, pk=team_id)
    members = team.get_all_members()
    if team.accomodation_status == 'confirmed':
        for member in members:
            member.accomod_is_confirmed = False
            member.save()
    team.accomodation_status = 'not_req'
    team.save()
    messages.success(request, 'Accommodation request cancelled successfully!')
    users=[]
    for user in team.get_all_members():
        users.append(user.email)
    mail.send(
        users, template='email/hospi/cancel_accommodation',
        context={'team':team,}
        )
    return redirect('hospi_prehome')

def delete_team(request, team_id):
    if not request.session.get('saaranguser_email'):
        messages.error(request, 'Please login to continue')
        return redirect('hospi_login')
    email = request.session.get('saaranguser_email')
    user = SaarangUser.objects.get(email=email)
    team = get_object_or_404(HospiTeam, pk=team_id)
    users=[]
    for user in team.get_all_members():
        users.append(user.email)
    mail.send(
        users, template='email/hospi/team_deleted',
        context={'team':team,}
        )
    team.delete()
    messages.success(request, 'Team has been successfully deleted')
    return redirect('hospi_prehome')

def generate_saar(request, team_id):
    if not request.session.get('saaranguser_email'):
        return redirect('hospi_login')
    email = request.session.get('saaranguser_email')
    user = SaarangUser.objects.get(email=email)
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
        'addUserForm':SaarangUserForm(),
        'editable':editable,
        'team':team,
    }
    return render(request, 'hospi/team_details.html', to_return)

@login_required
def print_saar(request, team_id):
    return u.generate_pdf(request, team_id)

@login_required
def split_team(request, team_id):
    team = get_object_or_404(HospiTeam, pk=team_id)
    M=['male', 'Male']
    F=['female', 'Female']
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
    return redirect('hospi_list_registered_teams')

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
        emailsubject='Accommodation request '+stat+', Saarang 2014'
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
    base = 'SA2014A'
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

@login_required
def check_in_males(request):
    data = request.POST.copy()
    team = get_object_or_404(HospiTeam, pk=data['team_id'])
    males = team.get_male_members()
    for male in males:
        room = get_object_or_404(Room, pk=data[male.saarang_id])
        room.occupants.add(male)
        room.save()
        HospiLog.objects.create(created_by=request.user, user=male, room=room)
    team.checked_in = True
    team.mattress_count=data['matress']
    team.save()
    messages.success(request, team.team_sid + ' checked in successfully')
    return redirect('hospi_list_registered_teams')

@login_required
def check_in_females(request):
    data = request.POST.copy()
    team = get_object_or_404(HospiTeam, pk=data['team_id'])
    females = team.get_female_members()
    for female in females:
        room = get_object_or_404(Room, pk=data[female.saarang_id])
        room.occupants.add(female)
        room.save()
        HospiLog.objects.create(created_by=request.user, user=female, room=room)
    team.checked_in = True
    team.mattress_count=data['matress']
    team.save()
    messages.success(request, team.team_sid + ' checked in successfully')
    return redirect('hospi_list_registered_teams')

@login_required
def check_out_team(request, team_id):
    team = get_object_or_404(HospiTeam, pk=team_id)
    members = team.members.all()
    try:
        room = team.leader.room_occupant.all()[0]
        room.occupants.remove(team.leader)
        room.save()
        log_entry = HospiLog.objects.get(user=team.leader)
        log_entry.checked_out = True
        log_entry.checkout_time = datetime.datetime.now()
        log_entry.checked_out_by = request.user
        log_entry.save()
    except:
        return u.checkout_bill(request, team_id)
    for member in members:
        try:
            room = member.room_occupant.all()[0]
            room.occupants.remove(member)
            room.save()
            log_entry = HospiLog.objects.get(user=member)
            log_entry.checked_out = True
            print log_entry
            log_entry.checkout_time = datetime.datetime.now()
            log_entry.checked_out_by = request.user
            log_entry.save()
        except Exception, e:
            return u.checkout_bill(request, team_id)
    team.checked_out = True
    team.save()
    messages.success(request, team.team_sid + ' checked out successfully')
    return redirect('hospi_list_registered_teams')

@login_required
def print_bill(request, team_id):
    return u.checkout_bill(request, team_id)
    
@csrf_exempt
@login_required
def update_member(request):
    data = request.POST.copy()
    user = get_object_or_404(SaarangUser, pk=int(data['id']))
    setattr(user, data['columnName'], data['value'])
    user.save()
    return HttpResponse(data['value'])

@login_required
def add_member(request,team_id):
    team = HospiTeam.objects.get(pk=team_id)
    if request.method == 'POST':
        userform =SaarangUserForm(request.POST)
        print request.POST
        if userform.is_valid():
            user = userform.save()
            user.saarang_id = uid(user.pk)
            characters = string.ascii_letters + string.punctuation  + string.digits
            password =  "".join(choice(characters) for x in range(randint(8, 16)))
            user.password = password
            user.activate_status = 2
            user.save()
            team.members.add(user)
            team.save()
            mail.send(
                [user.email], template='email/main/activate_confirm',
                context={'saarang_id':user.saarang_id, 'password':user.password}
            )
            messages.success(request, 'User added successfully')
        else:
            print "Invalid"
    return redirect('hospi_team_details', team.pk)

@csrf_exempt
@login_required
def del_member(request, team_id):
    team = HospiTeam.objects.get(pk=team_id)
    data = request.POST.copy()
    user = get_object_or_404(SaarangUser, pk=int(data['id']))
    team.members.remove(user)
    user.save()
    team.save()
    return HttpResponse('ok')

@csrf_exempt
@login_required
def website_id_search(request):
    data=request.GET.copy()
    user_list = []
    users_id = SaarangUser.objects.filter(saarang_id__contains=data['q'].upper())[:10]
    users_email = SaarangUser.objects.filter(email__contains=data['q'].lower())[:10]
    users_name = SaarangUser.objects.filter(name__contains=data['q'])[:10]
    users_mobile = SaarangUser.objects.filter(mobile__contains=data['q'])[:10]
    for user in users_id:
        user_list.append({"id":user.id,'sid':user.saarang_id, 'email':user.email, 'name':user.name, 'mobile':user.mobile })
    for user in users_email:
        user_list.append({"id":user.id,'sid':user.saarang_id, 'email':user.email, 'name':user.name, 'mobile':user.mobile })
    for user in users_name:
        user_list.append({"id":user.id,'sid':user.saarang_id, 'email':user.email, 'name':user.name, 'mobile':user.mobile })
    for user in users_mobile:
        user_list.append({"id":user.id,'sid':user.saarang_id, 'email':user.email, 'name':user.name, 'mobile':user.mobile })
    user_dict = json.dumps(user_list)
    return HttpResponse(user_dict)

@login_required
def add_user_to_team(request):
    data = request.POST.copy()
    try:
        team = get_object_or_404(HospiTeam, pk=int(data['team_id']))
        user = get_object_or_404(SaarangUser, pk=int(data['website_id']))
        team.members.add(user)
        team.save()
        messages.success(request, 'User added successfully')
    except:
        messages.error(request, 'Error, please try again!!')
    return redirect('hospi_team_details', int(data['team_id']))

@login_required
def delete_room(request, room_id):
    room = Room.objects.get(pk=room_id)
    return HttpResponse('Under construction')