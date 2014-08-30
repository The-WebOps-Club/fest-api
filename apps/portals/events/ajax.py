# For simple dajax(ice) functionalities
from django.utils import simplejson
import json
from dajaxice.decorators import dajaxice_register

# For rendering templates
from django.template import RequestContext
from django.template.loader import render_to_string

# Decorators
from django.contrib.auth.decorators import login_required, user_passes_test


#models
from django.contrib.auth.models import User
from apps.users.models import ERPProfile, UserProfile, Dept, Subdept
from apps.portals.events.models import EventTab, Event
#dajaxice stuff
from dajaxice.utils import deserialize_form



@dajaxice_register
def hello(request):
    return json.dumps({'message': 'aslkfhas'})






@dajaxice_register
def show_tabs(request,event_name,username):
    event_object=Event.objects.get(name=event_name)
    user_object=User.objects.get(username=username)
    has_perm = permission(event_object,user_object)
    print has_perm
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
    return json.dumps({'description': description,'event_name':event_name,'event_tab_name': event_tab.name,'has_perm':has_perm})


#Function for setting permissions to edit Event Tabs 
def permission(event_object,user_object):
	events_dept=Dept.objects.get(name='events')
	qms_dept=Dept.objects.get(name='qms')
	if hasattr(user_object,'erp_profile'):
		a=5
	else:
		if event_object.has_tdp:
			return "participant_event_has_tdp"
		else:
			return "participant"
	if events_dept in user_object.erp_profile.core_relations.all() or qms_dept in user_object.erp_profile.core_relations.all():
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
def delete_tab(request,event_name,event_tab_name):
    event_object=Event.objects.get(name=event_name)
    event_tab=EventTab.objects.get(name=event_tab_name,event=event_object)
    event_tab.delete()
    return json.dumps({'message':'The event-tab '+event_tab_name+' from the event '+event_name+' has been deleted'})





@dajaxice_register
def add_tab(request,add_tab_form):
    add_tab_form=deserialize_form(add_tab_form)
    message=""
    if add_tab_form['tab_name']!='' and  add_tab_form['tab_name'][0]!=' ':
		event_tab=EventTab()
		event_tab.name=add_tab_form['tab_name']
		event_tab.content=add_tab_form['tab_description']
		event_tab.event=Event.objects.get(name=add_tab_form['event_name'])
		event_tab.save()
		message="The " + add_tab_form['tab_name'] + " tab has been successfully added to the " + add_tab_form['event_name'] + " event"
    return json.dumps({'message': message})



@dajaxice_register
def edit_tab(request,edit_tab_form):
    edit_tab_form=deserialize_form(edit_tab_form)
    message=""
    if edit_tab_form['tab_Name']!='' and  edit_tab_form['tab_Name'][0]!=' ':
			event_object=Event.objects.get(name=edit_tab_form['event_Name_edit_form'])
			event_Tab=EventTab.objects.get(name=edit_tab_form['event_tab_Name_edit_form'],event=event_object)
			event_Tab.delete()

			event_tab=EventTab()
			event_tab.name=edit_tab_form['tab_Name']
			event_tab.content=edit_tab_form['tab_Description']
			event_tab.event=Event.objects.get(name=edit_tab_form['event_Name_edit_form'])
			event_tab.save()

			message="The " + edit_tab_form['tab_Name'] + " tab from the event " + edit_tab_form['event_Name_edit_form'] + "  has been successfully Edited."

    return json.dumps({'message': message})
    
    
    
@dajaxice_register
def edit_event_details(request,event_name):
	event_object=Event.objects.get(name=event_name)
	return json.dumps({'message': 'message','event_name':event_name,'short_description':event_object.short_description,'event_type':event_object.event_type,'category':event_object.category,'has_tdp':event_object.has_tdp,'team_size_min':event_object.team_size_min,'team_size_max':event_object.team_size_max,'registration_starts':event_object.registration_starts,'registration_ends':event_object.registration_ends,'google_group':event_object.google_group,'email':event_object.email})
    
    
#try to make the deserialized form of the type addeventform then validate it

from apps.portals.events.forms import AddEventForm    
@dajaxice_register    
def add_event(request,event_form):
	message="Your form has the following errors\n"
	event_form = AddEventForm(deserialize_form(event_form))
	if event_form.is_valid():
		event_form.save()
		message="successfully added event"
	else:
		for field in event_form:
			for error in field.errors:
				message=message+field.html_name+" : "+error+"\n"
				
	return json.dumps({'message': message})
	

from django.core.exceptions import ValidationError
@dajaxice_register    
def edit_event(request,event_name,edit_event_form):
	message="Your form has the following errors\n"
	edit_event_form = deserialize_form(edit_event_form)
	message= "p"+str(edit_event_form['registration_starts'])+"p"
	event_object=Event.objects.get(name=event_name)

	return json.dumps({'message': message})
	
