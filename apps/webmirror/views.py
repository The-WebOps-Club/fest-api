from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
from apps.webmirror.models import DataBlob

from access_tokens import tokens, scope

def set_universal_access( response ):
	response["Access-Control-Allow-Origin"] = "*"  
	response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"  
	response["Access-Control-Max-Age"] = "1000"  
	response["Access-Control-Allow-Headers"] = "*"
	return response

@csrf_exempt
def set_data( request, pk ):
	blob = None
	data = request.POST['data']
	token = request.POST['token']
	cluster = None

	if( 'cluster' in request.POST ):
		cluster = request.POST['cluster']
	

	try:
		blob = DataBlob.objects.get( ref = format(pk), cluster = format(cluster) )
	except Exception:
		if( not tokens.validate( token, scope.access_all() ) ):
			return set_universal_access(HttpResponse(json.dumps({'msg':'NOAUTH'})))
		blob = DataBlob.objects.create( data = '', ref = format(pk), cluster = format(cluster) )

	if( not tokens.validate( token, scope.access_obj( blob ) ) ):
		return set_universal_access(HttpResponse(json.dumps({'msg':'NOAUTH'})))
	
	blob.data = data
	blob.save()

	return set_universal_access(HttpResponse(json.dumps({'msg':'DONE'})))
	

def get_data( request, pk ):

	response = None;
	try:
		blob = DataBlob.objects.get( ref = format(pk) )
	except Exception:
		return set_universal_access(HttpResponse(json.dumps({'msg':'NOBLOB','content':'Webmirror Exception: No data'})))

	return set_universal_access(HttpResponse(json.dumps({'msg':'DONE','content':blob.data})))

def get_cluster( request, cluster ):

	response = None;
	try:
		blobs = DataBlob.objects.filter( cluster = format(cluster) )
	except Exception:
		return set_universal_access(HttpResponse(json.dumps({'msg':'NOBLOB','content':'Internal Error'})))

	data = {};
	for i in blobs:
		data[i.ref] = i.data

	return set_universal_access(HttpResponse(json.dumps({'msg':'DONE','data':data})))