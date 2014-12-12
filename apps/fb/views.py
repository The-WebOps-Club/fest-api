# Django
from django.shortcuts import get_object_or_404, render_to_response, redirect, HttpResponseRedirect, render, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.templatetags.static import static
from django.utils.http import int_to_base36, base36_to_int
# Apps
from misc.utils import *  #Import miscellaneous functions
from misc import strings

def opc(request):
    local_context = {
    }
    return render_to_response("pages/fb/opc.html", local_context, context_instance= global_context(request, token_info=False))
