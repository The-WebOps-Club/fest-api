# Django
from django.template.context import Context, RequestContext
from django.shortcuts import HttpResponseRedirect, resolve_url
from django.core.urlresolvers import reverse, resolve
from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.utils.encoding import force_str
from django.utils.timezone import utc
from django.conf import settings
# Decorators
# Apps
import apps
from misc.managers import *
from misc.strings import *  #Import miscellaneous functions
from misc.exceptions import *  #Import miscellaneous functions
from misc.decorators import *  #Import miscellaneous functions
from apps.docs.utils import Drive, Github, Calendar
# Models
from django.db import models
from django.contrib.auth.models import User, Group
# Forms
# View functions
# Misc
# Python
from functools import wraps
import datetime
import json

# ------------------ TEMPLATE CUSTOMIZATIONS
#----------------------------------------------------------------------
# Generates a context with the most used variables
def global_context(request, token_info=True, user_info=True):
    """
        Some basic variables useful in templates
        Usage : add context_instance=global_context(request) to the kwargs of the response function
    """
    erp_profile = None
    profile = None
    drive_folders = []
    calendars = []
    if user_info and hasattr(request.user, "erp_profile"):
    	erp_profile = request.user.erp_profile if hasattr(request.user, "erp_profile") else None
    	drive_folders = []
    	calendars = []
        if erp_profile:
            entity_list = list(erp_profile.coord_relations.all()) + \
                    list(erp_profile.supercoord_relations.all()) + \
                    list(erp_profile.page_relations.all())
            if list(erp_profile.core_relations.all()):
                entity_list += list(apps.users.models.Dept.objects.all())
            for entity in entity_list:
                drive_folders.append(
                    (entity.name, entity.directory_id)
                )
		try:
		    calendars.append((entity.name, entity.calendar_id))
		except Exception,e:
		    pass
		print calendars
        if hasattr(request.user, "profile"):
        	profile = request.user.profile
    	else:
        	profile = None
    # token = None
    # if token_info and settings.USE_EXTERNAL_SITES:
    # 	drive = Drive()
    # 	token = Drive.get_access_token()
    
    local_context = {
        'user' : request.user,
        'erp_profile' : erp_profile,
        'user_profile' : profile,
        'session' : request.session,
        # 'google_access_token' : token,
        'drive_folders': drive_folders,
        'calendars' : calendars,
        'experimental' : settings.EXPERIMENTAL_MODE,
        'SITE_URL' : settings.SITE_URL,
        'FEST_NAME' : settings.FEST_NAME,
        'SETTINGS' : settings,
    }

    # Handle experimental mode.
    if 'experimental' in request.GET.keys(): # Take from get
        request.session['experimental'] = request.GET['experimental']
    if ('experimental' in request.session.keys()): # Take from preset value
        local_context['experimental'] = request.session['experimental']
    print local_context["experimental"]
    context =  RequestContext(request, local_context)
    return context

# ------------------ FORM CUSTOMIZATIONS
#----------------------------------------------------------------------
def make_custom_datefield(f, **kwargs):
    """
        This makes it easy for datepickr fron jquery to be added to a django form
        Just add :
            formfield_callback = make_custom_datefield
        inside the django form
    """
    formfield = f.formfield(**kwargs)
    if isinstance(f, models.DateField):
        #print formfield
        formfield.widget.format = '%m/%d/%Y'
        formfield.widget.attrs.update({'class':'datePicker'})#, 'readonly':'true'})
    return formfield

# ------------------ VALIDITY CHECKS
#----------------------------------------------------------------------
def valid_phone_number(num_string):
    """
        Takes a phone number string and checs if the thing is a valid phone number.
        Returns True or False
    """
    data = "".join(num_string.split()).replace("+", "")
    return data.isdigit() and len(data) >= 10 and len(data) <= 13 


# ------------------ SIMPLE UTILS
#----------------------------------------------------------------------

# A small helper class to create custom attributes
class Bunch:
    def __init__(self, **kwds):
        self.__dict__.update(kwds)
