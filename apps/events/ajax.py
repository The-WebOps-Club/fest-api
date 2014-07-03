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



from apps.events.models import EventTab, Event
from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
@dajaxice_register
def show_tabs(request,event_name):
    event_object=Event.objects.get(name=event_name)
    tabs_object_list=event_object.eventtab_set.all()
#tabs_names_list is a string with a set of event-tab-names -separated by commas
    tabs_names_list=''
    for i in tabs_object_list:
	tabs_names_list=tabs_names_list+i.name+','
    return simplejson.dumps({'tabs_names_list':'%s' % tabs_names_list,'event_name':event_name})


@dajaxice_register
def show_tabs_description(request,event_name,event_tab):
    event_object=Event.objects.get(name=event_name)
    event_tab=EventTab.objects.get(name=event_tab,event=event_object)
    description=event_tab.content
    return simplejson.dumps({'description': description,'event_name':event_name,'event_tab_name': event_tab.name})




