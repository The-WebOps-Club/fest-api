from django.shortcuts import render
from django.shortcuts import render_to_response
from misc.utils import global_context

def portal_main( request ):
	return render_to_response('portals/events/events.html', {}, context_instance = global_context(request))