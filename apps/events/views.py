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

@csrf_exempt
@api_view(['GET'])
@permission_classes((AllowAny, ))
def my_events(request):
	data = request.DATA
	user_id = data.get('user_id', None)
	event_name = data.get('event_name', None)

	user = User.objects.filter(id=user_id)
	event = Event.objects.filter(name=event_name)
	if ( len(event) != 0 ):
		event = event[0]
		event.participants_registered.add(user)
		event.save()
		return Response({
			"success": "You have registered for the event"
		}, status=status.HTTP_202_ACCEPTED)
	return Response({
		"error": "There seems to be an error. We cannot find this event in our list. Please contact the webops team : <a href='mailto:webops@shaastra.org'>webops@shaastra.org</a>"
	}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny, ))
def add_participant(request):
	data = request.DATA
	user_id = data.get('user_id', None)
	event_name = data.get('event_name', None)

	user = User.objects.filter(id=user_id)
	event = Event.objects.filter(name=event_name)
	if ( len(event) != 0 ):
		event = event[0]
		event.participants_registered.add(user)
		event.save()
		return Response({
			"success": "You have registered for the event"
		}, status=status.HTTP_202_ACCEPTED)
	return Response({
		"error": "There seems to be an error. We cannot find this event in our list. Please contact the webops team : <a href='mailto:webops@shaastra.org'>webops@shaastra.org</a>"
	}, status=status.HTTP_400_BAD_REQUEST)
	
@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny, ))
def add_team(request, team_id, event_name):
	data = request.DATA
	team_id = data.get('team_id', None)
	event_name = data.get('event_name', None)

	team = Team.objects.filter(id=team_id)
	event = Event.objects.filter(name=event_name)
	if ( len(event) != 0 ):
		event = event[0]
		event.teams_registered.add(team)
		event.save()
		return Response({
			"success": "You team has registered for the event"
		}, status=status.HTTP_202_ACCEPTED)
	return Response({
		"error": "There seems to be an error. We cannot find this event in our list. Please contact the webops team : <a href='mailto:webops@shaastra.org'>webops@shaastra.org</a>"
	}, status=status.HTTP_400_BAD_REQUEST)
