# For simple dajax(ice) functionalities
from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax

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
from misc.utils import *
from apps.users.models import *
from apps.walls.models import *
from post_office import mail

import os
from django.core.management import call_command

def admins_only(in_func):
    def out_func(request, *args, **kwargs):
        if not request.user.is_staff:
            return json.dumps({'message':'Not Authorized'})
        in_func(request, *args, **kwargs )
    return out_func

@dajaxice_register
def hello_world(request):
    """
        Used for testing Dajax + Dajaxice
    """
    dajax = Dajax()
    dajax.assign('body','innerHTML', "Hello world !")
    #dajax.alert("Hello World!")
    return dajax.json()
    
@dajaxice_register
def hello(request):
    """
        Used for testing Dajaxice
    """
    #html_content = render_to_string("dash/task_tables/coord_you.html", query_dictionary, RequestContext(request))
    return json.dumps({'message': 'hello'})

########## FOR ADMIN PORTAL #######################
@dajaxice_register
def get_users_of_subdept(request, subdept_id):
    user = request.user
    if not user.is_staff:
        return json.dumps({'message':'Not Authorized'})

    append_string = ""
    for i in ERPProfile.objects.filter(coord_relations__in=Subdept.objects.filter(id=subdept_id)):
        append_string+=render_to_string('portals/general/user.html', {'user':i.user,'link_type':'subdept','link_id':subdept_id}, context_instance=global_context(request, token_info=False))
    return json.dumps({'append_string':append_string});

@dajaxice_register
def get_users_of_page(request, page_id):
    user = request.user
    if not user.is_staff:
        return json.dumps({'message':'Not Authorized'})

    append_string = ""
    for i in ERPProfile.objects.filter(page_relations__in=Page.objects.filter(id=page_id)):
        append_string+=render_to_string('portals/general/user.html', {'user':i.user,'link_type':'page','link_id':page_id}, context_instance=global_context(request, token_info=False))
    return json.dumps({'append_string':append_string});

@dajaxice_register
def add_users_to_page(request,page_id,user_ids):
    user = request.user
    if not user.is_staff:
        return json.dumps({'message':'Not Authorized'})

    page = Page.objects.get(id = page_id)
    append_string = ''
    for user_id in user_ids:
        e = User.objects.get(id = user_id.split('_')[1]).erp_profile
        if not (page in e.page_relations.all()):
            append_string += render_to_string('portals/general/user.html', {'user':e.user,'link_type':'page','link_id':page_id}, context_instance=global_context(request, token_info=False))
        e.page_relations.add(page)

    return json.dumps({'message':'done','append_string':append_string})

@dajaxice_register
def add_users_to_subdept(request,subdept_id,user_ids):
    user = request.user
    erp_profile = user.erp_profile
    if not user.is_staff:
        return json.dumps({'message':'Not Authorized'})

    subdept = Subdept.objects.get(id = subdept_id)
    dept = subdept.dept

    append_string = ''
    if erp_profile.core_relations.filter(id=dept.id).count() == 0 and \
        erp_profile.supercoord_relations.filter(id=dept.id).count() == 0:
        return json.dumps({'message': 'This subdept is not under your department !'})

    for user_id in user_ids:
        e = User.objects.get(id = user_id.split('_')[1]).erp_profile
        if not (subdept in e.coord_relations.all()):
            append_string += render_to_string('portals/general/user.html', {'user':e.user,'link_type':'subdept','link_id':subdept_id}, context_instance=global_context(request, token_info=False))
        e.coord_relations.add(subdept)

    return json.dumps({'message':'done','append_string':append_string})

@dajaxice_register
def delete_user_from_subdept(request,subdept_id,user_id):
    user = request.user
    erp_profile = user.erp_profile
    if not user.is_staff:
        return json.dumps({'message':'Not Authorized'})

    subdept = Subdept.objects.get(id = subdept_id)
    dept = subdept.dept
    if erp_profile.core_relations.filter(id=dept.id).count() == 0 and \
        erp_profile.supercoord_relations.filter(id=dept.id).count() == 0:
        return json.dumps({'message': 'This subdept is not under your department !'})

    User.objects.get(id = user_id).erp_profile.coord_relations.remove(subdept)
    return json.dumps({'message':'done'})
    pass

@dajaxice_register
def delete_user_from_page(request,page_id,user_id):
    user = request.user
    if not user.is_staff:
        return json.dumps({'message':'Not Authorized'})

    User.objects.get(id = user_id).erp_profile.page_relations.remove(Page.objects.get(id = page_id))
    return json.dumps({'message':'done'})
    pass

@dajaxice_register
def create_subdept(request, dept_id, name):
    user = request.user
    if not user.is_staff:
        return json.dumps({'message':'Not Authorized'})

    if user.erp_profile.core_relations.filter(id=dept_id).count() == 0 and user.erp_profile.supercoord_relations.filter(id=dept_id).count() == 0:
        return json.dumps({'message': 'This subdept is not under your department !'})

    s = Subdept.objects.create(dept=Dept.objects.get(id=dept_id), name=name)
    return json.dumps({'message' : 'done', 'id' : s.id, 'name' : name})

@dajaxice_register
def create_page(request, name):
    # ?
    user = request.user
    if not user.is_staff:
        return json.dumps({'message':'Not Authorized'})

    p = Page.objects.create(name=name);
    return json.dumps({'message': 'done', 'id' : p.id, 'name' : name})

@dajaxice_register
def remove_subdept(request, subdept_id):
    # ?
    user = request.user
    erp_profile = user.erp_profile
    if not user.is_staff:
        return json.dumps({'message':'Not Authorized'})

    subdept = Subdept.objects.get(id = subdept_id)
    dept = subdept.dept
    if erp_profile.core_relations.filter(id=dept.id).count() == 0 and \
        erp_profile.supercoord_relations.filter(id=dept.id).count() == 0:
        return json.dumps({'message': 'This subdept is not under your department !'})

    Subdept.objects.get(id=subdept_id).delete();
    return json.dumps({'message': 'done'})

@dajaxice_register
def remove_page(request, page_id):
    user = request.user
    erp_profile = user.erp_profile
    if not user.is_staff:
        return json.dumps({'message':'Not Authorized'})

    Page.objects.get(id = page_id).delete();
    return json.dumps({'message':'done'})

@dajaxice_register
def create_user(request, username, email, first_name, last_name):
    user = request.user
    erp_profile = user.erp_profile
    if not user.is_staff:
        return json.dumps({'message':'Not Authorized'})

    if( User.objects.filter(email = email).count() ):
        return json.dumps({'message':'Account with ' + email + ' already exists'});

    if( User.objects.filter(username = username).count() ):
        return json.dumps({'message':'Account with ' + username + ' already exists'});

    passwd = User.objects.make_random_password()
    u = User.objects.create(username = username, email = email, first_name =  first_name, last_name = last_name, password=passwd);
    e = ERPProfile.objects.create(user=u)
    if settings.SEND_EMAIL:
        mail.send( [u.email], 
            settings.DEFAULT_FROM_EMAIL, 
            template='welcome.email',
            context={ 
                'user' : u,
                'password' : passwd,
                'SITE_URL' : settings.SITE_URL,
                'FEST_NAME' : settings.FEST_NAME,
            },
            headers = {},
        )
        # print "Error : The email id", e.user.email, "was not found. UserProfile id : ", e.id
    # refresh json lists.
    call_command('jsonify_data')
    call_command('collectstatic',interactive=False)
    
    return json.dumps( { 
        'message' : 'Successfully created <b>' + username + '</b> Email has been sent with the password to the given email address.',
        'passkey' : passwd
    } )
