# For simple dajax(ice) functionalities
from dajaxice.decorators import dajaxice_register

# For rendering templates
from django.template import RequestContext
from django.template.loader import render_to_string
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from configs import settings
from apps.users.models import Dept, Subdept, ERPProfile
from apps.walls.models import Wall, Post, Comment

from apps.walls.utils import get_tag_object
from annoying.functions import get_object_or_None
# Decorators
from django.contrib.auth.decorators import login_required, user_passes_test
import json
from misc.utils import *
from apps.users.models import *
from apps.walls.models import *
from post_office import mail

import os
from django.core.management import call_command

    
@dajaxice_register
def hello(request):
    """
        Used for testing Dajaxice
    """
    #html_content = render_to_string("dash/task_tables/coord_you.html", query_dictionary, RequestContext(request))
    return json.dumps({'message': 'hello'})

########## FOR ADMIN PORTAL #######################
