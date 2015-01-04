# Utility functions
import datetime as dt

def cd(n):
    '''Returns caution deposit'''
    if n%2 == 0:
        return 500*(n/2)
    elif n%2 == 1:
        return 500*((n+1)/2)
def days(in_date, in_time, out_date, out_time):
    l1 = dt.datetime(2015, 1, 7, 10, 0)
    u1 = dt.datetime(2015, 1, 8, 17, 0)
    l2 = dt.datetime(2015, 1, 8, 5, 0)
    u2 = dt.datetime(2015, 1, 9, 17, 0)
    l3 = dt.datetime(2015, 1, 9, 5, 0)
    u3 = dt.datetime(2015, 1, 10, 17, 0)
    l4 = dt.datetime(2015, 1, 10, 5, 0)
    u4 = dt.datetime(2015, 1, 11, 17, 0)
    l5 = dt.datetime(2015, 1, 11, 5, 0)
    u5 = dt.datetime(2015, 1, 12, 9, 0)
    
    span = [[l1,u1],[l2,u2],[l3,u3],[l4,u4],[l5,u5]]

    in_stamp = dt.datetime.combine(in_date, in_time)
    out_stamp = dt.datetime.combine(out_date, out_time)

    for i in xrange(0,5):
        if (in_stamp >= span[i][0] and in_stamp <= span[i][1] and in_stamp<span[i+1][0] ):
            for j in xrange(i,5):
                if out_stamp >= span[j][0] and out_stamp <= span[j][1]:
                    return j-i+1
    return 0

def bill(in_date, in_time, out_date, out_time, n):
    '''Calculate bill amount'''
    dos = days(in_date,in_time,out_date,out_time)
    diff_rate = 300
    days_of_stay = dos
    amt_per_head = 300 + diff_rate*(days_of_stay-1)
    amt_without_caution_deposit = ((300 + diff_rate*(days_of_stay-1))*n)
    caution_deposit = cd(n)
    total_amt =  ( ((300 + diff_rate*(days_of_stay-1))*n) + cd(n) )
    return {
        'days':dos,
        'amt_head':amt_per_head,
        'total':amt_without_caution_deposit,
        'cd':caution_deposit,
        'grand_total':total_amt,
    }


from xhtml2pdf import pisa
import os
from django.conf import settings
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from models import HospiTeam
from django.shortcuts import render, redirect, get_object_or_404


# Convert HTML URIs to absolute system paths so xhtml2pdf can access those resources
def link_callback(uri, rel):
    # use short variable names
    sUrl = settings.STATIC_URL      # Typically /static/
    sRoot = settings.STAT    # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL       # Typically /static/media/
    mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/

    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))

    elif uri.startswith(sUrl):
        print uri
        print sRoot
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
        print path
    # make sure that file exists
    if not os.path.isfile(path):
            raise Exception(
                    'media URI must start with %s or %s' % \
                    (sUrl, mUrl))

    return path

def generate_pdf(request, team_id):
    # Prepare context
    team = get_object_or_404(HospiTeam, pk=team_id)
    leader = team.leader
    members = team.members.all().order_by('-gender')
    bill_data = bill(team.date_of_arrival, team.time_of_arrival, team.date_of_departure, team.time_of_departure, team.get_total_count())
    data = {
        'leader':leader,
        'team':team,
        'members':members,
        'bill_data':bill_data,
    }

    # Render html content through html template with context
    template = get_template('portals/hospi/saar.html')
    html  = template.render(Context(data))

    # Write PDF to file
    file = open(os.path.join(settings.MEDIA_ROOT, 'SAAR_'+team.team_sid+'.pdf'), "w+b")
    pisaStatus = pisa.CreatePDF(html, dest=file,
            link_callback = link_callback)

    # Return PDF document through a Django HTTP response
    file.seek(0)
    pdf = file.read()
    file.close()            # Don't forget to close the file handle
    response =  HttpResponse(pdf, mimetype='application/pdf')
    # response['Content-Disposition'] = "attachment; filename='SAAR_"+team.team_sid+"_Saarang2014.pdf'"
    return response


def checkout_bill(request, team_id):
    team = get_object_or_404(HospiTeam, pk=team_id)
    leader = team.leader
    members = team.members.all().order_by('gender')
    bill_data = bill(team.date_of_arrival, team.time_of_arrival, team.date_of_departure, team.time_of_departure, team.get_total_count())
    rooms=[]
    for member in members:
        room = member.room_occupant.all()
        for roo in room:
            rooms.append([roo.name,roo.hostel]) 
    data = {
        'leader':leader,
        'team':team,
        'members':members,
        'bill_data':bill_data,
        'rooms':rooms,
    }
    # Render html content through html template with context
    template = get_template('portals/hospi/check_out_bill.html')
    html  = template.render(Context(data))

    # Write PDF to file
    file = open(os.path.join(settings.MEDIA_ROOT, 'Reciept_'+team.team_sid+'.pdf'), "w+b")
    pisaStatus = pisa.CreatePDF(html, dest=file,
            link_callback = link_callback)

    # Return PDF document through a Django HTTP response
    file.seek(0)
    pdf = file.read()
    file.close()            # Don't forget to close the file handle
    response =  HttpResponse(pdf, mimetype='application/pdf')
    # response['Content-Disposition'] = "attachment; filename='Bill_"+team.team_sid+"_Saarang2014.pdf'"
    return response

