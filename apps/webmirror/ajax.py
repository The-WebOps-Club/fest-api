# For simple dajax(ice) functionalities
from dajaxice.decorators import dajaxice_register
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
from apps.webmirror.models import DataBlob

from access_tokens import tokens, scope
@dajaxice_register
def set_data( request, pk, data, token ):

	blob = None
	try:
		blob = DataBlob.objects.get( pk = pk )
	except Exception:
		blob = DataBlob.objects.create( data = '' )

	if( not tokens.validate( token, scope.access_obj( blob ) ) ):
		return json.dumps({'msg':'NOAUTH'})

	blob.data = data
	blob.save()
	return json.dumps({'msg':'DONE'})

@dajaxice_register
def get_data( request, pk ):

	try:
		blob = DataBlob.objects.get( pk = pk )
	except Exception:
		return json.dumps({'msg':'NOBLOB','content':'Webmirror Exception: No data'})

	return json.dumps({'msg':'DONE','content':blob.data})