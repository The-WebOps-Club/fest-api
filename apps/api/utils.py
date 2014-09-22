from django.http import HttpResponse, HttpResponseBadRequest

from social.apps.django_app.utils import strategy, load_strategy
from apps.users.models import UserProfile
from rest_framework.authtoken.models import Token

def viewset_response(message,data):
	temp={}	
	temp['status']=0
	temp['message']=message
	temp['data']=data	
	if not message:
		temp['status']=1
		temp['message']='success'
	return temp
	

def mobile_auth(request, backend, *args, **kwargs):
    try:
        access_token = request.GET.get('access_token')
    except Exception, e:
        raise HttpResponseBadRequest('An access_token needs to be provided.')

    strat = load_strategy(backend=backend)
    backend = strat.backend

    try:
        user = backend.do_auth(access_token=access_token)
    except:
        return HttpResponse('Unauthorized', status=401)

    try:
        userprofile = user.profile
        upid=userprofile.id
    except Exception, e:
        # Create and save a userprofile
        userprofile = UserProfile(user=user)
        userprofile.save()
        try:
            token=Token.objects.create(user=user)
        except Exception, e:
            pass
    data = {
        'username' : user.username,
        'userid' : user.id,
        'token' : token,
        'userprofileid' : upid,
        'email' : user.email,
    }
    data = json.dumps(data)
    return HttpResponse(data, mimetype="application/json")
