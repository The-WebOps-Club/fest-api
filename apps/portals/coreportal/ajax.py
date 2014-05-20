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

def cores_only(in_func):
    def out_func(request, *args, **kwargs):
        if not (request.session['role'] == 'Core'):
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

@dajaxice_register
def get_users_of_subdept(request, subdept_id):
    if not (request.session['role'] == 'core'):
        return json.dumps({'message':'Not Authorized'})

    append_string = ""
    for i in ERPProfile.objects.filter(coord_relations__in = [Subdept.objects.filter(id = subdept_id)[0]] ):
        append_string+=render_to_string('portals/coreportal/user.html', {'user':i.user,'link_type':'subdept','link_id':subdept_id}, context_instance=global_context(request, token_info=False))
    return json.dumps({'append_string':append_string});

@dajaxice_register
def get_users_of_page(request, page_id):
    if not (request.session['role'] == 'core'):
        return json.dumps({'message':'Not Authorized'})

    append_string = ""
    for i in ERPProfile.objects.filter(page_relations__in = [Page.objects.filter(id = page_id)[0]] ):
        append_string+=render_to_string('portals/coreportal/user.html', {'user':i.user,'link_type':'page','link_id':page_id}, context_instance=global_context(request, token_info=False))
    return json.dumps({'append_string':append_string});

@dajaxice_register
def add_users_to_page(request,page_id,user_ids):
    if not (request.session['role'] == 'core'):
        return json.dumps({'message':'Not Authorized'})

    append_string = ''
    for user_id in user_ids:
        e = ERPProfile.objects.get(id = user_id.split('_')[1])
        if not (page in e.page_relations.all()):
            append_string+=render_to_string('portals/coreportal/user.html', {'user':e.user,'link_type':'page','link_id':page_id}, context_instance=global_context(request, token_info=False))
        e.page_relations.add(Page.objects.get(id = page_id))
        

    return json.dumps({'message':'done','append_string':append_string})

@dajaxice_register
def add_users_to_subdept(request,subdept_id,user_ids):
    if not (request.session['role'] == 'core'):
        return json.dumps({'message':'Not a core :P'})

    subdept = Subdept.objects.get(id = subdept_id)

    append_string = ''
    if not (request.session['role_dept'] == subdept.dept.id):
        return json.dumps({'message':'Not your subdept :P'})

    for user_id in user_ids:
        e = ERPProfile.objects.get(id = user_id.split('_')[1])
        if not (subdept in e.coord_relations.all()):
            append_string+=render_to_string('portals/coreportal/user.html', {'user':e.user,'link_type':'subdept','link_id':subdept_id}, context_instance=global_context(request, token_info=False))        
        e.coord_relations.add(subdept)

    return json.dumps({'message':'done','append_string':append_string})

@dajaxice_register
def delete_user_from_subdept(request,subdept_id,user_id):
    if not (request.session['role'] == 'core'):
        return json.dumps({'message':'Not Authorized'})

    subdept = Subdept.objects.get(id = subdept_id)
    if not (request.session['role_dept'] == subdept.dept.id):
        return json.dumps({'message':'Not your subdept :P'})

    ERPProfile.objects.get(id = user_id).coord_relations.remove(subdept)
    return json.dumps({'message':'done'})
    pass

@dajaxice_register
def delete_user_from_page(request,page_id,user_id):
    if not (request.session['role'] == 'core'):
        return json.dumps({'message':'Not Authorized'})

    ERPProfile.objects.get(id = user_id).page_relations.remove(Page.objects.get(id = page_id))
    return json.dumps({'message':'done'})
    pass

@dajaxice_register
def create_subdept(request, dept_id, page_name):
    # ?
    if not (request.session['role'] == 'core'):
        return json.dumps({'message':'Not Authorized'})

    if not (request.session['role_dept'] == dept_id):
        return json.dumps({'message':'Not your subdept :P'})

    s = Subdept();
    s.dept_id = dept_id
    s.name = page_name
    s.save();
    return json.dumps({'message':'done','id':s.id,'name':page_name})

@dajaxice_register
def create_page(request, page_name):
    # ?
    if not (request.session['role'] == 'core'):
        return json.dumps({'message':'Not Authorized'})

    p = Page();
    p.name = page_name;
    p.save();
    return json.dumps({'message':'done','id':p.id,'name':page_name})

@dajaxice_register
def remove_subdept(request, subdept_id):
    # ?
    if not (request.session['role'] == 'core'):
        return json.dumps({'message':'Not Authorized'})

    subdept = Subdept.objects.get(id = subdept_id)
    if not (request.session['role_dept'] == subdept.dept.id):
        return json.dumps({'message':'Not your subdept :P'})

    Subdept.objects.get(id = subdept_id).delete();
    return json.dumps({'message':'done','id':s.id,'name':page_name})

@dajaxice_register
def remove_page(request, page_id):
    # ?
    if not (request.session['role'] == 'core'):
        return json.dumps({'message':'Not Authorized'})

    Page.objects.get(id = dept_id).delete();
    return json.dumps({'message':'done','id':p.id,'name':page_name})