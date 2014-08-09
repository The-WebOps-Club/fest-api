# For simple dajax(ice) functionalities
from dajaxice.decorators import dajaxice_register

# For rendering templates
from django.template import RequestContext
from django.template.loader import render_to_string

from django.contrib.auth.models import User
from configs import settings
from apps.users.models import Dept, Subdept, ERPProfile
from apps.walls.models import Wall, Post, Comment

from apps.walls.utils import get_tag_object
from annoying.functions import get_object_or_None
# Decorators
from django.contrib.auth.decorators import login_required, user_passes_test
import json
    
@dajaxice_register
def hello(request):
    """
        Used for testing Dajaxice
    """
    #html_content = render_to_string("dash/task_tables/coord_you.html", query_dictionary, RequestContext(request))
    return json.dumps({'message': 'hello'})

@dajaxice_register
def get_contact(request, id):
    """
        Sends contact information about the id
    """
    obj = get_object_or_None(User, id=int(id))
    if isinstance(obj, User):
        obj_profile = obj.profile
        obj_erp_profile = obj.erp_profile
        local_context = {
            "id" : obj.id,
            "email" : obj.email,
	    	"mobile_number" : obj_profile.mobile_number,
	    	"summer_number" : obj_erp_profile.summer_number,
        }
    else:
    	local_context = {
            "id" : "",
            "mobile_number" : "",
            "summer_number" : "",
            "email" : "",
        }
    return json.dumps(local_context)

@dajaxice_register
def get_info(request, id):
    """
        Sends contact information about the id
    """
    obj = get_object_or_None(User, id=int(id))
    if isinstance(obj, User):
        obj_profile = obj.profile
        obj_erp_profile = obj.erp_profile
        local_context = {
            "id" : obj.id,
            "email" : obj.email,
            "fbid" : obj_profile.fbid,
        }
    else:
    	local_context = {
            "id" : "",
            "email" : "",
            "fbid" : "",
        }
    return json.dumps(local_context)



from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form

from apps.users.forms import UserProfileForm
from django.contrib.auth.models import User
from apps.users.models import  UserProfile

from django.contrib.auth import authenticate, login


from django.utils import simplejson
from dajaxice.decorators import dajaxice_register

@dajaxice_register
def participant_registration(request,username,user_profile_form):
    message="Your form has the following errors <br />\n"
    alert_message="The form has errors. Error details are at the top of the registration form"
    login_success="no"
    
    user_profile_form = UserProfileForm(deserialize_form(user_profile_form))
    forms_successfully_validated=0
    
    #validating user_profile_form
    if user_profile_form.is_valid():
		forms_successfully_validated=1
    else:
		for field in user_profile_form:
			for error in field.errors:
			    message=message+field.html_name+" : "+error+"<br />\n"
	
	
	
	



    if forms_successfully_validated==1:
		message=''
		new_user=User.objects.get(username=username)  
		new_user_profile=UserProfile()
		new_user_profile.gender= user_profile_form.cleaned_data['gender']
		new_user_profile.dob= user_profile_form.cleaned_data['dob']
		new_user_profile.mobile_number= user_profile_form.cleaned_data['mobile_number']
		new_user_profile.branch= user_profile_form.cleaned_data['branch']
		new_user_profile.college= user_profile_form.cleaned_data['college']
		new_user_profile.college_roll= user_profile_form.cleaned_data['college_roll']
		new_user_profile.school_student= user_profile_form.cleaned_data['school_student']
		new_user_profile.want_accomodation= user_profile_form.cleaned_data['want_accomodation']
		new_user_profile.user=new_user
		new_user_profile.save()
		login_success="yes"
		new_user.is_active=True
		alert_message="Registered successfully"
    
    return simplejson.dumps({'message': message,'alert_message':alert_message,'login_success':login_success})






        
