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
