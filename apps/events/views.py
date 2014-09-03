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
from apps.webmirror.utils import make_global_token
from django.shortcuts import render_to_response
from misc.utils import global_context


from apps.events.models import Event, EventTab
from django.contrib.auth.decorators import login_required

@login_required
def add_tabs( request ):
	message=""
	events=Event.objects.all()
	event_list=[]
	for i in events:
		event_list=event_list+[i.name]
	

	context_dict = {'event_list':event_list,'message':message}
	return render_to_response('events/events2.html', context_dict, context_instance = global_context(request))




