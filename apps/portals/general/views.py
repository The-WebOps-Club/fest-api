from django.shortcuts import render
from apps.walls.models import Wall
from apps.users.models import ERPProfile, Dept, Subdept, Page
from django.shortcuts import get_object_or_404, render_to_response, redirect, HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from misc.utils import *
from itertools import chain

# Create your views here.
def admin_portal(request):
    user = request.user
    erp_profile = user.erp_profile
    if not user.is_staff:
        raise PermissionDenied('You are not allowed here.')

    depts = list(chain(erp_profile.supercoord_relations.all(), erp_profile.core_relations.all()))
    if user.is_superuser:
        depts = Dept.objects.all()
        
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
    print depts
    return render_to_response('portals/general/admin_portal.html', local_context, context_instance= global_context(request))
