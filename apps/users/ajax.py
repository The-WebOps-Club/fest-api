# For simple dajax(ice) functionalities
from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax

# For rendering templates
from django.template import RequestContext
from django.template.loader import render_to_string

from django.contrib.auth.models import User
from configs import settings
from apps.users.models import Dept, Subdept, ERPProfile
from apps.walls.models import Wall, Post, Comment

from apps.walls.utils import get_tag_object
from annoying.functions import get_object_or_None
# Decorators
from django.contrib.auth.decorators import login_required, user_passes_test
import json

@dajaxice_register
def hello_world(request):
    """
        Used for testing Dajax + Dajaxice
    """
    dajax = Dajax()
    dajax.assign('body','innerHTML', "Hello world !")
    #dajax.alert("Hello World!")
    return dajax.json()
    
@dajaxice_register
def hello(request):
    """
        Used for testing Dajaxice
    """
    #html_content = render_to_string("dash/task_tables/coord_you.html", query_dictionary, RequestContext(request))
    return json.dumps({'message': 'hello'})

@dajaxice_register
def get_contact(request, id):
    """
        Sends contact information about the id
    """
    obj = get_object_or_None(User, id=int(id))
    if isinstance(obj, User):
        obj_profile = obj.profile
        obj_erp_profile = obj.erp_profile
        local_context = {
            "id" : obj.id,
            "email" : obj.email,
	    	"mobile_number" : obj_profile.mobile_number,
	    	"summer_number" : obj_erp_profile.summer_number,
        }
    else:
    	local_context = {
            "id" : "",
            "mobile_number" : "",
            "summer_number" : "",
            "email" : "",
        }
    return json.dumps(local_context)

@dajaxice_register
def get_info(request, id):
    """
        Sends contact information about the id
    """
    obj = get_object_or_None(User, id=int(id))
    if isinstance(obj, User):
        obj_profile = obj.profile
        obj_erp_profile = obj.erp_profile
        local_context = {
            "id" : obj.id,
            "email" : obj.email,
            "fbid" : obj_profile.fbid,
        }
    else:
    	local_context = {
            "id" : "",
            "email" : "",
            "fbid" : "",
        }
    return json.dumps(local_context)
