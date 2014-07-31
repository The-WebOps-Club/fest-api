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
def portal_main2( request ):
	message=""
#If add tab button was pressed
	if request.method == 'POST' and "addNewTab" in request.POST:
		if request.POST['tab_name']!='' and  request.POST['tab_name'][0]!=' ':
			print "yuu"
	    		event_tab=EventTab()
			event_tab.name=request.POST['tab_name']
			event_tab.content=request.POST['tab_description']
			event_tab.event=Event.objects.get(name=request.POST['event_name'])
			event_tab.save()
			message="The " + request.POST['tab_name'] + " tab has been successfully added to the " + request.POST['event_name'] + " event"
#If delete tab button was pressed	    
	if request.method == 'POST' and "delete_tab" in request.POST:
		print "dd"
		event_object=Event.objects.get(name=request.POST['eventName'])
		event_tab=EventTab.objects.get(name=request.POST['event_tab_name'],event=event_object)
		event_tab.delete()
    		message="The "+ request.POST['event_tab_name']+" tab in the event " + request.POST['eventName']+ " has been successfully deleted"
#If edit tab button was pressed
	if request.method == 'POST' and "EditTab" in request.POST:
		if request.POST['tab_Name']!='' and  request.POST['tab_Name'][0]!=' ':
			event_object=Event.objects.get(name=request.POST['event_Name_edit_form'])
			event_Tab=EventTab.objects.get(name=request.POST['event_tab_Name_edit_form'],event=event_object)
			event_Tab.delete()

			event_tab=EventTab()
			event_tab.name=request.POST['tab_Name']
			event_tab.content=request.POST['tab_Description']
			event_tab.event=Event.objects.get(name=request.POST['event_Name_edit_form'])
			event_tab.save()

			print "qqqqqqqqu"
			message="The " + request.POST['tab_Name'] + " tab from the event " + request.POST['event_Name_edit_form'] + "  has been successfully Edited."


	events=Event.objects.all()
	event_list=[]
	for i in events:
		event_list=event_list+[i.name]
	

	context_dict = {'event_list':event_list,'message':message}
	return render_to_response('events/events2.html', context_dict, context_instance = global_context(request))
