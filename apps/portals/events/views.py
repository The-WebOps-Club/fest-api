# Django
from django.shortcuts import render_to_response, redirect, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.conf import settings
# Apps
from misc.utils import *  #Import miscellaneous functions
# Decorators
# Models
from django.contrib.auth.models import User
# Forms
# View functions
# Misc
from django.templatetags.static import static
# Python
import os

from django.shortcuts import render
from django.shortcuts import render_to_response
from misc.utils import global_context

#models
from django.contrib.auth.models import User
from apps.users.models import ERPProfile, UserProfile, Dept, Subdept
from apps.events.models import Event, EventTab
from django.contrib.auth.decorators import login_required
from apps.portals.events.forms import AddEventForm

@login_required
def add_tabs( request ):
	message=""
	event_form=AddEventForm()
	events=Event.objects.all()

	core_perm=None
	
	if request.user.is_staff:
		core_perm=1
	

	context_dict = {'event_list':events,'message':message,'event_form':event_form,'core_perm':core_perm}
	return render_to_response('events/events2.html', context_dict, context_instance = global_context(request))

@login_required
def portal_main( request ):
	print PORTAL_NAME
	return render_to_response('portals/events/events.html', {}, context_instance = global_context(request))

