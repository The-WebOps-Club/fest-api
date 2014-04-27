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
from misc.strings import *  #Import miscellaneous functions
from misc.exceptions import *  #Import miscellaneous functions
from misc.decorators import *  #Import miscellaneous functions
from apps.docs.utils import Drive, Github
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
def global_context(request):
    """
        Some basic variables useful in templates
        Usage : add context_instance=global_context(request) to the kwargs of the response function
    """
    from apps.users.models import Dept, Subdept
    erp_profile = request.user.erp_profile if hasattr(request.user, "erp_profile") else None
    if hasattr(request.user, "profile"):
        profile = request.user.profile 
    else:
        profile = None
    drive = Drive()
    token = Drive.get_access_token()
    local_context = {
        'user':request.user,
        'erp_profile':erp_profile,
        'user_profile':profile,
        'session':request.session,
        'current_path':request.get_full_path(),
        'google_access_token' : token,
        'SITE_URL':settings.SITE_URL,
        'MEDIA_URL':settings.MEDIA_URL,
        'MEDIA_ROOT':settings.MEDIA_ROOT,
        'STATIC_ROOT':settings.STATIC_ROOT,
        'STATIC_URL':settings.STATIC_URL,
        'DEBUG':settings.DEBUG,
        'SETTINGS':settings,
        'FEST_NAME':settings.FEST_NAME,
    }

    context =  RequestContext (request, local_context)
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
