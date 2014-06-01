# For simple dajax(ice) functionalities
from dajaxice.decorators import dajaxice_register
# From Django
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers

# For rendering templates
from django.template import RequestContext
from django.template.loader import render_to_string

# Decorators
from django.contrib.auth.decorators import login_required, user_passes_test
import json

from haystack.query import SearchQuerySet

@dajaxice_register
def hello(request, query):
    """
        Used for testing Dajaxice
    """
    #html_content = render_to_string("dash/task_tables/coord_you.html", query_dictionary, RequestContext(request))
    return json.dumps({'query': query})

@dajaxice_register
def query(request, query):
	results = SearchQuerySet().filter(content=query)
	results_list = [q.get_stored_fields() for q in results]
	return json.dumps(results_list)