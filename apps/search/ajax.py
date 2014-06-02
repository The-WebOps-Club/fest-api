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

from apps.walls.utils import get_my_posts

@dajaxice_register
def hello(request, query):
    """
        Used for testing Dajaxice
    """
    #html_content = render_to_string("dash/task_tables/coord_you.html", query_dictionary, RequestContext(request))
    return json.dumps({'query': query})

@dajaxice_register
def query(request, query):
	user = request.user
	results = SearchQuerySet().filter(content=query)
	results_list = [q.get_stored_fields() for q in results]
	accessible_posts_id = [post.id for post in get_my_posts(user)]
	for post in results_list:
		if post['post_id'] not in accessible_posts_id:
			results_list.remove(post)
	return json.dumps(results_list)