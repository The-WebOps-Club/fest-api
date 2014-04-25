# For simple dajax(ice) functionalities
from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax

# For rendering templates
from django.template import RequestContext
from django.template.loader import render_to_string

from apps.walls.utils import get_tag_object

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
def get_phone(request, id, tag):
    """
        Used for testing Dajaxice
    """
    obj = get_tag_object(tag)
    local_context = {
    	"mobile_number" : obj.profile.mobile_number,
    	"summer_number" : obj.erp_profile.summer_number,
    }
    return json.dumps(local_context)
