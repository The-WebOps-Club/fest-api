from django.shortcuts import render
from apps.walls.models import Wall
from apps.users.models import ERPProfile, Dept, Subdept, Page
from django.shortcuts import get_object_or_404, render_to_response, redirect, HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.http import Http404
from misc.utils import *
#from itertools import chain
from django.conf import settings
import time, datetime
from .__init__ import PORTAL_NAME
    
# Create your views here.
def finance_portal(request):
    if PORTAL_NAME not in settings.OPEN_PORTALS:
        raise Http404
    user = request.user
    link_list = []
    erp_profile = user.erp_profile
    position = erp_profile.get_position(request) 
    date = datetime.date.today().strftime('%Y-%m-%d')
    relations = list() + list(erp_profile.supercoord_relations.all()) + list(erp_profile.coord_relations.all())
    for core in erp_profile.core_relations.all():
        position = core.name + " Core for Saarang 2015"
        dept = core.name
        link = settings.GOOGLE_FORMS['finance_fest'] %(dept, position, erp_profile.name,user.profile.mobile_number, user.email, date  )
        link_list.append((position,link))
        
    for supercoord in erp_profile.supercoord_relations.all():
        position = supercoord.name + " SuperCoord for Saarang 2015"
        dept = supercoord.name
        link = settings.GOOGLE_FORMS['finance_fest'] %(dept, position, erp_profile.name,user.profile.mobile_number, user.email, date  )
        link_list.append((position, link))

    for coord in erp_profile.coord_relations.all():
        position = coord.dept.name +'('+ coord.name + ')' + " Coord for Saarang 2015"
        dept = coord.dept.name
        link = settings.GOOGLE_FORMS['finance_fest'] %(dept, position, erp_profile.name,user.profile.mobile_number, user.email, date  )
        link_list.append((position, link))

    position = "Lit-Soc / Cultural Clubs"
    club = " "	
    link = settings.GOOGLE_FORMS['finance_clubs'] %(club, position, erp_profile.name,user.profile.mobile_number, user.email, date  )
    link_list.append((position, link))
    local_context = {
            "list":link_list,
            "current_page":"portal_finance"
    }
    return render_to_response('portals/finance/finance_portal.html', local_context, context_instance= global_context(request))

