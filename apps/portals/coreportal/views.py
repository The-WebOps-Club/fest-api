from django.shortcuts import render
from apps.walls.models import *
from apps.users.models import *
from django.shortcuts import get_object_or_404, render_to_response, redirect, HttpResponseRedirect
from misc.utils import *

# Create your views here.

def coreportal(request):
	# permissions.
	if not(request.session['role'] == 'core'):
		raise PermissionDenied('YOU SHALL NOT PASS.')

	local_context = {
		'subdepts': [],
		'pages':Page.objects.all(),
		'users':ERPProfile.objects.all(),
	}

	dept = Dept.objects.get(id = request.session['role_dept'])
	local_context['subdepts'].append({'dept':dept,'subdepts':dept.subdepts.all()})

	return render_to_response('portals/coreportal/coreportal.html', local_context, context_instance= global_context(request))
