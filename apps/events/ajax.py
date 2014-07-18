# For simple dajax(ice) functionalities
from django.utils import simplejson
from dajaxice.decorators import dajaxice_register

# For rendering templates
from django.template import RequestContext
from django.template.loader import render_to_string

# Decorators
from django.contrib.auth.decorators import login_required, user_passes_test


@dajaxice_register
def hello(request):
    """
        Used for testing Dajaxice
    """
    #html_content = render_to_string("dash/task_tables/coord_you.html", query_dictionary, RequestContext(request))
    return simplejson.dumps({'message': 'hello'})



#dajaxice stuff
from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
#models
from django.contrib.auth.models import User
from apps.users.models import ERPProfile, UserProfile, Dept, Subdept
from apps.events.models import EventTab, Event



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
    return simplejson.dumps({'tabs_names_list':'%s' % tabs_names_list,'event_name':event_name,'has_perm':has_perm})


@dajaxice_register
def show_tabs_description(request,event_name,event_tab,has_perm):
    event_object=Event.objects.get(name=event_name)
    event_tab=EventTab.objects.get(name=event_tab,event=event_object)
    description=event_tab.content
    return simplejson.dumps({'description': description,'event_name':event_name,'event_tab_name': event_tab.name,'has_perm':has_perm})


#Function for setting permissions to edit Event Tabs 
def permission(event_object,user_object):
	events_dept=Dept.objects.get(name='events')
	qms_dept=Dept.objects.get(name='qms')
	if hasattr(user_object,'erp_profile'):
		a=5
	else:
		return "no"
	if events_dept in user_object.erp_profile.core_relations.all() or qms_dept in user_object.erp_profile.core_relations.all():
		return "yes"
	else:
		return "no"

