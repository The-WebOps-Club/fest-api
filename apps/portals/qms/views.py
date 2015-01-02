from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from apps.walls.models import Wall
from apps.users.models import ERPProfile, Dept, Subdept, Page,UserProfile,Team
from django.contrib.auth.models import User
from misc.models import College
from apps.events.models import EventRegistration

from apps.users.forms import LoginForm,UserForm
from apps.portals.qms.forms import AddTeamForm,UserProfileForm,AddEventRegistrationForm

from django.shortcuts import get_object_or_404, render_to_response, redirect, HttpResponseRedirect
from django.http import HttpResponse

from django.core.exceptions import PermissionDenied
from misc.utils import *
from itertools import chain
#
# Create your views here.
def erp_analytics(request):
    """
        This is incomplete.
    """
    user = request.user
    erp_profile = user.erp_profile
    
    if not user.is_staff:
        raise PermissionDenied('You are not allowed here.')

    depts = list(chain(erp_profile.supercoord_relations.all(), erp_profile.core_relations.all()))
    local_context = {
        'dept_info': [{
            'dept' : dept,
            'subdepts' : dept.subdepts.all(),
        } for dept in depts],
        'pages' : Page.objects.all(),
        'users' : ERPProfile.objects.all(),

        'erp_profile_count' : ERPProfile.objects.count(),
        'dept_count' : Dept.objects.count(), 
        'subdept_count' : Subdept.objects.count(), 
        'page_count' : Page.objects.count(), 
           
    }
    return render_to_response('portals/general/admin_portal.html', local_context, context_instance= global_context(request))
    
@login_required   
def qms_portal(request):
    user_form = UserForm()
    user_profile_form = UserProfileForm()
    teamform = AddTeamForm()
    registrationform=AddEventRegistrationForm()
    to_return={'userform':user_form,'userprofileform':user_profile_form,'teamform':teamform,'registrationform':registrationform}
    return render(request, 'portals/qms/qms.html', to_return)
    
    
@login_required
def id_search(request):
    data=request.GET.copy()
    user_list = []
    selected_users=[]
    users_id = UserProfile.objects.filter(saarang_id__contains=data['q'].upper())[:10]
    users_email = UserProfile.objects.filter(user__email__contains=data['q'].lower())[:10]
    users_name = UserProfile.objects.filter(name__contains=data['q'])[:10]
    users_mobile = UserProfile.objects.filter(mobile_number__contains=data['q'])[:10]
    
    
    for user in users_id:
        selected_users=selected_users+[user]
    for user in users_email:
        selected_users=selected_users+[user]
    for user in users_name:
        selected_users=selected_users+[user]
    for user in users_mobile:
        selected_users=selected_users+[user]
    selected_users=set(selected_users)
    
    for user in selected_users:
        user_list.append({"desk_id":user.desk_id,'id':user.user.id,'saarang_id':user.saarang_id, 'email':user.user.email, 'first_name':user.user.first_name,'last_name':user.user.last_name, 'mobile_number':user.mobile_number, 'city':user.city,  'branch':user.branch, 'college_text':user.college_text, 'age':user.age, 'want_accomodation':user.want_accomodation, 'gender':user.gender.capitalize() })
    user_dict = json.dumps(user_list)
    return HttpResponse(user_dict)


'''
@login_required
def id_search(request):
    data=request.GET.copy()
    user_list = []
    users_id = UserProfile.objects.filter(saarang_id__contains=data['q'].upper())[:10]
    users_email = UserProfile.objects.filter(email__contains=data['q'].lower())[:10]
    users_name = UserProfile.objects.filter(name__contains=data['q'])[:10]
    users_mobile = UserProfile.objects.filter(mobile_number__contains=data['q'])[:10]
    for user in users_id:
        user_list.append({"desk_id":user.desk_id,'saarang_id':user.saarang_id, 'email':user.email, 'name':user.name, 'mobile':user.mobile, 'city':user.city, 'college':user.college.name, 'gender':user.gender.capitalize() })
    for user in users_email:
        user_list.append({"desk_id":user.desk_id,'saarang_id':user.saarang_id, 'email':user.email, 'name':user.name, 'mobile':user.mobile, 'city':user.city, 'college':user.college.name, 'gender':user.gender.capitalize() })
    for user in users_name:
        user_list.append({"desk_id":user.desk_id,'saarang_id':user.saarang_id, 'email':user.email, 'name':user.name, 'mobile':user.mobile, 'city':user.city, 'college':user.college.name, 'gender':user.gender.capitalize() })
    for user in users_mobile:
        user_list.append({"desk_id":user.desk_id,'saarang_id':user.saarang_id, 'email':user.email, 'name':user.name, 'mobile':user.mobile, 'city':user.city, 'college':user.college.name, 'gender':user.gender.capitalize() })
    user_dict = json.dumps(user_list)
    for user in user_list:
    	print user
    return HttpResponse(user_dict)
'''


#'members':team.members,

@login_required
def team_search(request):
    data=request.GET.copy()
    team_list=[]
    selected_teams=[]
    teams = Team.objects.filter(name__contains=data['q'])[:10]
    teams2 = Team.objects.filter(name__contains=data['q'].upper())[:10]
 	
    for t in teams:
 		selected_teams = selected_teams + [t]
    for t in teams2:
 		selected_teams = selected_teams + [t]
    selected_teams=set(selected_teams)
 	
    for team in selected_teams:
        team_list.append({"name":team.name,'id':team.id,'accomodation_status':team.accomodation_status})
    team_dict = json.dumps(team_list)
    return HttpResponse(team_dict)
