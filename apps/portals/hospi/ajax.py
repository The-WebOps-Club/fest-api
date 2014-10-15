# For rendering templates
from django.template import RequestContext
from django.template.loader import render_to_string
import json
from dajaxice.decorators import dajaxice_register

@dajaxice_register
def registered_teams(request):
    html_content = render_to_string('portals/hospi/registered_teams.html', {}, RequestContext(request))
    return json.dumps({'html_content':html_content})