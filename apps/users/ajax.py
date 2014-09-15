# For simple dajax(ice) functionalities
from dajaxice.decorators import dajaxice_register
from django.utils import simplejson
from dajaxice.utils import deserialize_form

# For rendering templates
from django.template import RequestContext
from django.template.loader import render_to_string

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from configs import settings
from apps.users.models import Dept, Subdept, ERPProfile, UserProfile
from apps.walls.models import Wall, Post, Comment
from apps.users.forms import UserProfileForm

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

@dajaxice_register
def participant_registration(request, first_name, last_name, username, password):
	user = get_object_or_None(User, username=username)
	if user: # Oops someone already exists
		profile = get_object_or_None(UserProfile, user=user)
		if profile:
			return json.dumps({
				'status': 'error',
				'message': 'User already exists.'
			})						
		else:
			return json.dumps({
				'status': 'error',
				'message': 'User already exists. But profile not yet created'
			})
	user = User.objects.create_user(username, username, password)
	user.first_name = first_name
	user.last_name = last_name
	#new_user_profile = UserProfile.create()
	user.save()
	return json.dumps({
			'status': 'success',
			'message': 'User created.'
		})

@dajaxice_register
def participant_profile(request,username,user_profile_form):
	message = "Your form has the following errors <br />\n"
	alert_message = "The form has errors. Error details are at the top of the registration form"
	login_success = "no"
	
	user_profile_form = UserProfileForm(deserialize_form(user_profile_form))
	forms_successfully_validated = 0
	
	# validating user_profile_form
	if user_profile_form.is_valid():
		forms_successfully_validated=1
	else:
		for field in user_profile_form:
			for error in field.errors:
				message=message+field.html_name+" : "+error+"<br />\n"
	
	if forms_successfully_validated==1:
