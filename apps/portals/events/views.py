from django.shortcuts import render
from apps.webmirror.utils import make_global_token
from django.shortcuts import render_to_response
from misc.utils import global_context

def portal_main( request ):
	token = make_global_token()
	return render_to_response('portals/events/events.html', locals(), context_instance = global_context(request))