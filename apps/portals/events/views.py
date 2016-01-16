# Django
from django.shortcuts import render_to_response, HttpResponse, redirect, HttpResponseRedirect
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
import os, datetime
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.shortcuts import render
from django.shortcuts import render_to_response
from misc.utils import global_context
from apps.hospi.utility import link_callback
#models
from django.contrib.auth.models import User
from apps.users.models import ERPProfile, UserProfile, Dept, Subdept
from apps.events.models import Event, EventTab
from django.contrib.auth.decorators import login_required
from apps.portals.events.forms import AddEventForm, ImageEventForm
from apps.events.models import Event, EventWinner, EventSchedule

from apps.hospi.utility import render_pdf

@login_required
def add_tabs( request ):
    message=""
    event_form=AddEventForm()
    event_image_form=ImageEventForm()
    events=Event.objects.all()

    core_perm=None
    user_coordship_list=[]
    user_supercoordship_list=[]
    events_dept_object=Dept.objects.get(name='events')

    temp=request.user.erp_profile.coord_relations.all() 
    for i in temp:
        user_coordship_list=user_coordship_list+[i.dept]
        
    temp=request.user.erp_profile.supercoord_relations.all()
    for i in temp:
        user_supercoordship_list=user_supercoordship_list+[i.dept]

    
    if request.user.is_staff or events_dept_object in user_coordship_list or events_dept_object in user_supercoordship_list:
        core_perm=1
    if request.method == 'POST':
        form = ImageEventForm(request.POST, request.FILES)
        if form.is_valid():
            event = Event.objects.get(id=int(form.cleaned_data['event_id'])) 
            event.event_image = form.cleaned_data['image']
            event.save() 

    context_dict = {'event_list':events,'message':message,'event_form':event_form,'core_perm':core_perm,'event_image_form':event_image_form}
    return render_to_response('events/events2.html', context_dict, context_instance = global_context(request))

@login_required
def portal_main( request ):
    print PORTAL_NAME
    return render_to_response('portals/events/events.html', {}, context_instance = global_context(request))

@login_required
def generate_pdf_certificate(request, winner_id):
    if int(winner_id) is 0:
        winners = EventWinner.objects.all() 
    else:
        winners = EventWinner.objects.filter(id=winner_id)
    data={"winners":winners}
    return render_pdf(request, data, 'events/certif.html', 'CERTIF_'+winner_id+'.pdf')

def time_fn(val):
    val = int(str(val).lstrip('0'))
    return (((val+20)*2)/100)-18

@login_required
def generate_schedule(request):
    sched = EventSchedule.objects.order_by('slot_start')
    schedule = []
    for slot in sched:
        info={
            'slot': slot,
            'time':[0 for x in range(19)]
        }
        start_num = time_fn((slot.slot_start+datetime.timedelta(hours=5,minutes=30)).strftime('%H%M'))
        end_num = time_fn((slot.slot_end+datetime.timedelta(hours=5,minutes=30)).strftime('%H%M'))
        for i in range(19):
            if i>=start_num and i<=end_num:
                info['time'][i] = 1
        print info
        schedule.append(info)
    data = {
        'data':schedule
    }
    return render_pdf(request, data,'events/schedule.html','Schedule_Saarang2015.pdf')
    


