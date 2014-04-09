# For simple dajax(ice) functionalities
from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax

# From Django
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# For rendering templates
from django.template import RequestContext
from django.template.loader import render_to_string

# Decorators
from django.contrib.auth.decorators import login_required, user_passes_test
import json

from notifications.models import Notification
from misc.utils import *  #Import miscellaneous functions

# From Apps
from apps.walls.models import Post

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
