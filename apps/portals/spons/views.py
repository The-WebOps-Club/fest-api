# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.conf import settings

from apps.portals.spons.forms import AddLogoForm
from apps.spons.models import SponsImageUpload

def add_logo(request):
    if permission(request.user):    
        form = AddLogoForm(request.POST or None,request.FILES or None)
        if form.is_valid():
            img = form.save(commit=False)
            img.uploaded_by = request.user
            img.save()
            messages.success(request,'Image successfully saved')
            HttpResponseRedirect(reverse('spons_portal'))
        logos = SponsImageUpload.objects.all().order_by('-priority')
        to_return = {
            'form':form,
            'list':logos,
        }
        return render(request, 'portals/spons/add_logo.html', to_return)
    else :
        return render(request, 'portals/spons/perm.html')       

def delete_logo(request, logo_id):
    if permission(request.user):     
        logo=SponsImageUpload.objects.get(pk=logo_id)
        logo.delete()
        messages.success(request, 'Logo deleted successfully!')
        return redirect('spons_portal')
    else :
        return render(request, 'portals/spons/perm.html')
def edit_logo(request, logo_id):
    if permission(request.user):  
        logo=SponsImageUpload.objects.get(pk=logo_id)
        if request.method == 'POST':
            form = AddLogoForm(request.POST or None,request.FILES or None)
            if form.is_valid():
                img=form.save(commit=False)
                img.uploaded_by=request.user
                img.save()
                messages.success(request,'Image successfully updated')
                HttpResponseRedirect(reverse('spons_portal'))
        else:
            form = AddLogoForm(instance=logo)
        to_return={
            'logo':logo,
            'form': form,
        }
        return render(request, 'portals/spons/edit_logo.html', to_return)
    else :
        return render(request, 'portals/spons/perm.html')

def save_logo(request, logo_id):
    if permission(request.user): 
        logo=SponsImageUpload.objects.get(pk=logo_id)
        if request.method == 'POST':
            print 'POST'
            form = AddLogoForm(request.POST or None,request.FILES or None, instance=logo)
            print form.errors
            if form.is_valid():
                print 'valid'
                img=form.save(commit=False)
                img.uploaded_by=request.user
                img.save()
                messages.success(request,'Image successfully updated')
                return redirect('spons_portal')
    else :
        return render(request, 'portals/spons/perm.html')

def permission(user_object):
    if user_object.id in settings.SPONS_ACCESS_ID:
        return True
    return False
