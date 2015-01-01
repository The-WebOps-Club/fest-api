# For simple dajax(ice) functionalities
from django.utils import simplejson
import json
from pytz import timezone
import unicodedata
from dajaxice.decorators import dajaxice_register

# For rendering templates
from django.template import RequestContext
from django.template.loader import render_to_string

# Decorators
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings 

#models
from django.contrib.auth.models import User
from apps.users.models import ERPProfile, UserProfile, Dept, Subdept, Team
from apps.events.models import EventTab, Event, EventSchedule, EventWinner

from apps.portals.events.forms import AddSlotForm, EventWinnerForm

#dajaxice stuff
from dajaxice.utils import deserialize_form

import re

@dajaxice_register
def hello(request):
    return json.dumps({'message': 'aslkfhas'})






@dajaxice_register
def show_tabs(request,event_name,username):
    event_object=Event.objects.get(name=event_name)
    user_object=User.objects.get(username=username)
    has_perm = permission(event_object,user_object)
    tabs_object_list=event_object.eventtab_set.all()
#tabs_names_list is a string with a set of event-tab-names -separated by commas
    tabs_names_list=''
    for i in tabs_object_list:
	tabs_names_list=tabs_names_list+i.name+','
    return json.dumps({'tabs_names_list':'%s' % tabs_names_list,'event_name':event_name,'has_perm':has_perm})


@dajaxice_register
def show_tabs_description(request,event_name,event_tab,has_perm):
    event_object=Event.objects.get(name=event_name)
    event_tab=EventTab.objects.get(name=event_tab,event=event_object)
    description=event_tab.content
    description=" ".join(description.split())
    #print description
    return json.dumps({'description': description,'event_name':event_name,'event_tab_name': event_tab.name,'has_perm':has_perm})

#"<br/>".join(description.split("\r"))
#ARUN - CHANGES MADE HERE
#Function for setting permissions to edit Event Tabs 
def permission(event_object,user_object):
        return "yes"
	events_dept=Dept.objects.get(name='events')
	qms_dept=Dept.objects.get(name='qms')
	if hasattr(user_object,'erp_profile'):
		a=5
	else:
		if event_object.has_tdp:
			return "participant_event_has_tdp"
		else:
			return "participant"
	if user_object.is_staff or user_object.erp_profile in event_object.coords.all():
		return "yes"
	else:
		return "no"




@dajaxice_register
def register(request,event_name,username):
    user_object=User.objects.get(username=username)
    userprofile_object=UserProfile.objects.get(user=user_object)
    event_object=Event.objects.get(name=event_name)
    event_object.participants_registered.add(userprofile_object)
    event_object.save()
    return json.dumps({'message':event_name+username})


@dajaxice_register
def delete_tab(request,event_name,event_tab_name,username):
    event_object=Event.objects.get(name=event_name)
    event_tab=EventTab.objects.get(name=event_tab_name,event=event_object)
    event_tab.delete()
    return json.dumps({'message':'The event-tab '+event_tab_name+' from the event '+event_name+' has been deleted','username':username,'event_name':event_object.name})





@dajaxice_register
def add_tab(request,username,add_tab_form):
    add_tab_form=deserialize_form(add_tab_form)
    message=""    
    if add_tab_form['tab_name']!='' and  add_tab_form['tab_name'][0]!=' ':
		event_tab=EventTab()
		event_tab.name=add_tab_form['tab_name']
		event_tab.content=add_tab_form['tab_description']
		event_tab.event=Event.objects.get(name=add_tab_form['event_name'])
		event_tab.save()
		message="The " + add_tab_form['tab_name'] + " tab has been successfully added to the " + add_tab_form['event_name'] + " event"
    return json.dumps({'message': message,'username':username,'event_name':add_tab_form['event_name']})



@dajaxice_register
def edit_tab(request,username,edit_tab_form):
    edit_tab_form=deserialize_form(edit_tab_form)
    message=""
    if edit_tab_form['tab_Name']!='' and  edit_tab_form['tab_Name'][0]!=' ':
			event_object=Event.objects.get(name=edit_tab_form['event_Name_edit_form'])
			event_tab=EventTab.objects.get(name=edit_tab_form['event_tab_Name_edit_form'],event=event_object)

			event_tab.name=edit_tab_form['tab_Name']
			event_tab.content=edit_tab_form['tab_Description']
			event_tab.event=Event.objects.get(name=edit_tab_form['event_Name_edit_form'])
			event_tab.save()

			message="The " + edit_tab_form['tab_Name'] + " tab from the event " + edit_tab_form['event_Name_edit_form'] + "  has been successfully Edited."

    return json.dumps({'message': message,'username':username,'event_name':event_object.name})
    
    
from apps.portals.events.forms import AddEventForm    

@dajaxice_register
def edit_event_details(request,event_name):
	event_object=Event.objects.get(name=event_name)
	form = AddEventForm(instance=event_object).as_table()
	event_id = event_object.id
	try:
		image_source= str(event_object.event_image.url)
	except Exception,e:
		image_source=""
	
	slot_id=""
	slot_start=""
	slot_end=""
	slot_comment=""
	slot_venue=""

	try:
		event_slots= EventSchedule.objects.filter(event=event_object)
		for slot in event_slots:
			slot_id=slot_id+str(slot.id)+"|"
			slot_start=slot_start+((slot.slot_start).astimezone(timezone(settings.TIME_ZONE)).strftime('%c'))+"|"
			slot_end=slot_end+((slot.slot_end).astimezone(timezone(settings.TIME_ZONE)).strftime('%c'))+"|"
			slot_comment=slot_comment+ str(slot.comment) + "|" 
			slot_venue=slot_venue + str(slot.venue) + "|"
		length= len(event_slots)
	except Exception,e:
		pass

	winner_id=""
	winner_position=""
	winner_comment=""
	winner_added_by=""
	winner_user=""

	try:
		event_winners= EventWinner.objects.filter(event=event_object)
		for winner in event_winners:
			winner_id=winner_id+str(winner.id)+"|"
			winner_position=winner_position+(winner.position)+"|"
			winner_comment=winner_comment+(winner.comment)+"|"
			winner_added_by=winner_added_by+ str(winner.added_by) + "|" 
			winner_user=winner_user + str(winner.user) + "|"
		length_winner= len(event_winners)
	except Exception,e:
		pass
	return json.dumps({'form':form, 'message': 'message','event_name':event_name,'event_id':event_id,'image_source':image_source, 'slot_id':slot_id, 'slot_venue':slot_venue, 'slot_comment':slot_comment, 'slot_start':slot_start,'slot_end':slot_end,'length_count':length, 'winner_id':winner_id, 'winner_position':winner_position, 'winner_comment':winner_comment, 'winner_added_by':winner_added_by,'winner_user':winner_user, 'length_count_winner':length_winner})
    
    
@dajaxice_register
def display_add_event(request):
	form = AddEventForm().as_table()
	return json.dumps({'form':form})

#try to make the deserialized form of the type addeventform then validate it

@dajaxice_register    
def add_event(request,event_form):
	message="Your form has the following errors <br>"
	event_form = AddEventForm(deserialize_form(event_form))
	if event_form.is_valid():
		event_form.save()
		message="successfully added event"
	else:
		for field in event_form:
			for error in field.errors:
				message=message+field.html_name+" : "+error+"<br>"
				
	return json.dumps({'message': message})
	

from django.core.exceptions import ValidationError
@dajaxice_register    
def edit_event(request,event_name,edit_event_form):
	message="Your form has the following errors <br>"
	event_object=Event.objects.get(name=event_name)
	edit_event_form = AddEventForm(deserialize_form(edit_event_form), instance=event_object)
	if edit_event_form.is_valid():
		#event_object.name=edit_event_form.cleaned_data['name']
		#event_object.short_description=edit_event_form.cleaned_data['short_description']
		#event_object.event_type=edit_event_form.cleaned_data['event_type']
		#event_object.category =edit_event_form.cleaned_data['category']
		#event_object.has_tdp=edit_event_form.cleaned_data['has_tdp']
		#event_object.team_size_min=edit_event_form.cleaned_data['team_size_min']
		#event_object.team_size_max=edit_event_form.cleaned_data['team_size_max']
		#event_object.registration_starts=edit_event_form.cleaned_data['registration_starts']
		#event_object.google_group=edit_event_form.cleaned_data['google_group']
		#event_object.email=edit_event_form.cleaned_data['email']
		#event_object.coords=edit_event_form.cleaned_data['coords']
		#event_object.save()	
                edit_event_form.save()
		temp=1
		message="successfully added event"
	else:
		temp=0
		for field in edit_event_form:
			for error in field.errors:
				message=message+field.html_name+" : "+error+"<br>"


	return json.dumps({'message': message,'temp':temp})
	
	
	
	
	
@dajaxice_register    
def view_edit_event(request):
	event_names=""
	event_emails=""
	event_categories=""
	event_array=Event.objects.all()
	for event in event_array:
		event_names=event_names+event.name+"|"
		event_emails=event_emails+event.email+"|"
		event_categories=event_categories+event.category+"|"
	return json.dumps({'event_names': event_names,'event_emails':event_emails,'event_categories':event_categories})
	

@dajaxice_register    
def delete_event(request,event_name):
	event_object=Event.objects.get(name=event_name)
	event_object.delete()
	message="The event " + event_name + " has been successfully deleted."
	return json.dumps({'message':message})
	
	
	
@dajaxice_register    
def reg_list(request,event_name):
	event_object=Event.objects.get(name=event_name)
	event_registrations=event_object.event_registered.all()
	user_names=""
	team_names=""
	info=""
	for reg in event_registrations:
		user_names=user_names + reg.users_registered.username +" |"
		if reg.teams_registered==None:
			team_names=team_names + "None |"
		else:
			team_names=team_names + reg.teams_registered.name +" |"
		info=str(info) + str(reg.info) + " |"
	return json.dumps({'event_name':event_name,'user_names':user_names,'team_names':team_names,'info':info})

@dajaxice_register    
def participant_info(request,participant_name,team_name):

	try :
		data=[]
		temp={}		
		team = Team.objects.get(name=team_name)
		members=team.members.all()
		for i in range(len(members)):
			temp={}
			temp['name']=str(members[i].get_full_name())
			temp['number']=members[i].profile.mobile_number
			temp['email']=str(members[i].email)
			temp['college']= str(members[i].profile.college_text)
			temp['city']=str(members[i].profile.city)
			data.append(temp)
	except Exception, e:
		temp={}
		data=[]
		participant = User.objects.get(username=participant_name)
		temp['name']=str(participant_name)
		temp['number']=participant.profile.mobile_number
		temp['email']=str(participant.email)
		temp['college']= str(participant.profile.college_text)
		temp['city']=str(participant.profile.city)
		data.append(temp)
	return json.dumps({'inf':data,'len':len(data),})	


@dajaxice_register
def display_add_event_slot(request):
	form = AddSlotForm().as_table()
	slot_event=""
	slot_start=""
	slot_end=""
	slot_comment=""
	slot_venue=""
	slot_array = EventSchedule.objects.all()
	for slot in slot_array:
		slot_event=slot_event+slot.event.name+"|"
		slot_start=slot_start+((slot.slot_start).astimezone(timezone(settings.TIME_ZONE)).strftime('%c'))+"|"
		slot_end=slot_end+((slot.slot_end).astimezone(timezone(settings.TIME_ZONE)).strftime('%c'))+"|"
		slot_comment=slot_comment+ str(slot.comment) + "|" 
		slot_venue=slot_venue + str(slot.venue) + "|"
	return json.dumps({'form':form, 'slot_venue':slot_venue, 'slot_comment':slot_comment, 'slot_event': slot_event,'slot_start':slot_start,'slot_end':slot_end})

@dajaxice_register
def display_add_event_winner(request):
	form = EventWinnerForm().as_table()
	winner_id=""
	winner_position=""
	winner_comment=""
	winner_added_by=""
	winner_user=""
	winner_event=""
	event_winners= EventWinner.objects.all()
	for winner in event_winners:
		winner_id=winner_id+str(winner.id)+"|"
		winner_position=winner_position+(winner.position)+"|"
		winner_comment=winner_comment+(winner.comment)+"|"
		winner_added_by=winner_added_by+ str(winner.added_by) + "|" 
		winner_user=winner_user + str(winner.user) + "|"
		winner_event=winner_event + str(winner.event) + "|"
	length_winner= len(event_winners)
	return json.dumps({'form':form, 'winner_event':winner_event, 'winner_id':winner_id, 'winner_position':winner_position, 'winner_comment':winner_comment, 'winner_added_by':winner_added_by,'winner_user':winner_user, 'length_count_winner':length_winner})

    
@dajaxice_register    
def add_slot(request,slot_form):
	message="Your form has the following errors <br>"
	slot_form = AddSlotForm(deserialize_form(slot_form))
	if slot_form.is_valid():
		slot_form.save()
		message="successfully added event"
	else:
		for field in slot_form:
			for error in field.errors:
				message=message+field.html_name+" : "+error+"<br>"

	return json.dumps({'message': message})		

@dajaxice_register    
def delete_slot(request,slot_id):
	message="successfully Deleted slot"
	try:
		slot=EventSchedule.objects.get(id=int(slot_id))
		slot.delete()
	except Exception, e:
		message="no such slot exists"
	return json.dumps({'message': message})


@dajaxice_register    
def add_winner(request,winner_form):
	message="Your form has the following errors <br>"
	f = dict(deserialize_form(winner_form).iterlists())
	winner_form = EventWinnerForm((deserialize_form(winner_form)))
	obj = EventWinner()
	print 'here it is ' + str(int(f['event'][0]))
	obj.event = (Event.objects.get(id=int(f['event'][0])))
	obj.position = str(f['position'][0])
	obj.comment = str(f['comment'][0])
	obj.added_by = request.user.erp_profile
	obj.user = (UserProfile.objects.get(id=int(f['user'][0])))
	if winner_form.is_valid():
		obj.save()
		message="successfully added winner"
	else:
		for field in winner_form:
			for error in field.errors:
				message=message+field.html_name+" : "+error+"<br>"

	return json.dumps({'message': message})	

@dajaxice_register    
def delete_winner(request,winner_id):
	message="successfully Deleted winner"
	try:
		winner=EventWinner.objects.get(id=int(winner_id))
		winner.delete()
	except Exception, e:
		message="no such winner exists"
	return json.dumps({'message': message})
