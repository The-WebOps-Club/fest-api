from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
from apps.webmirror.models import DataBlob

from access_tokens import tokens, scope

@csrf_exempt
def set_data( request, pk ):
	blob = None
	data = request.POST['data']
	token = request.POST['token']

	try:
		blob = DataBlob.objects.get( pk = pk )
	except Exception:
		blob = DataBlob.objects.create( data = '' )

	if( not tokens.validate( token, scope.access_obj( blob ) ) ):
		return HttpResponse(json.dumps({'msg':'NOAUTH'}))

	blob.data = data
	blob.save()
	return HttpResponse(json.dumps({'msg':'DONE'}))


def get_data( request, pk ):

	try:
		blob = DataBlob.objects.get( pk = pk )
	except Exception:
		return HttpResponse(json.dumps({'msg':'NOBLOB','content':'Webmirror Exception: No data'}))

	return HttpResponse(json.dumps({'msg':'DONE','content':blob.data}))