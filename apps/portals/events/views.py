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
import os
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
from apps.events.models import Event, EventWinner
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
    template = get_template('events/certif.html')
    html  = template.render(Context(data))
    file = open(os.path.join(settings.MEDIA_ROOT, 'CERTIF_'+winner_id+'.pdf'), "w+b")
    pisaStatus = pisa.CreatePDF(html, dest=file, link_callback = link_callback)
    # Return PDF document through a Django HTTP response
    file.seek(0)
    pdf = file.read()
    file.close()            # Don't forget to close the file handle
    response =  HttpResponse(pdf, mimetype='application/pdf')
    # response['Content-Disposition'] = "attachment; filename='SAAR_"+team.team_sid+"_Saarang2014.pdf'"
    return response
    



