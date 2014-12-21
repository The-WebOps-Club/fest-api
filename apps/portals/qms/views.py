from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from apps.walls.models import Wall
from apps.users.models import ERPProfile, Dept, Subdept, Page,UserProfile
from django.contrib.auth.models import User

from apps.users.forms import LoginForm,UserProfileForm,UserForm
from apps.portals.qms.forms import AddTeamForm

from django.shortcuts import get_object_or_404, render_to_response, redirect, HttpResponseRedirect
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
    to_return={'userform':user_form,'userprofileform':user_profile_form,'teamform':teamform}
    return render(request, 'portals/qms/qms.html', to_return)
