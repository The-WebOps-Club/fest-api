from django.core.management.base import BaseCommand, CommandError, NoArgsCommand
from django.contrib.auth.models import User
from apps.users.models import Dept, Subdept, ERPProfile, Page
from django.conf import settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import datetime
import csv
import os
from post_office import mail
from smtplib import SMTPRecipientsRefused

SAMPLE_DEPTS = [
    'Design',
    'Events',
    'Facilities',
    'Finance',
    'QMS',
    'Hospitality',
    'Sponsorship',
    'WebOps'
]

class Command(BaseCommand):
    """
        Creates the department given in SAMPLE_DEPTS and add a core
        and two coordinators to the users for each dept.

        dept_core, dept_coord1 and dept_coord2

        Password is '1' for all the users

        If an arg is given, will populate db from that csv file
    """
    help = 'Automatically adds required entries into the database. esp Departments and Walls for them.'

    def handle(self, arg=None, commit=False, **options):
        # Department specific users
        
        if arg :
            arg_path = os.path.abspath(os.path.join(settings.PROJECT_PATH, arg))
            with open(arg_path, 'rb') as csvfile:
                csvreader = csv.reader(csvfile)#, delimiter=' ', quotechar='|')
                for i, row in enumerate(csvreader):
                    if i == 0 :
                        continue

                    self.stdout.write(">>> Processing ... row " + str(i) + " : " + str(row))
                    
                    if len(row) != 6:
                        print "[ERROR] Expected 6 rows."
                        continue

                    temp = User()
                    temp_erp_profile = ERPProfile()

                    email = row[0].strip() # User Email
                    fn = row[1].strip() # User Email
                    ln = row[2].strip() # User Email
                    core = [i.strip('"') for i in row[3].strip().split(":")] # Core Departments
                    sc = [i.strip('"') for i in row[4].strip().split(":")] # SuperCoord Departments
                    coord = [i.strip('"') for i in row[5].strip().split(":")] # Coord Departments

                    if fn and fn != "":
                        try:
                            validate_email(email)
                        except ValidationError:
                            self.stdout.write("[INVALID] E-Mail (according to django) : " + str(email))
                        temp.email = email
                        temp.username = email
                    else:
                        self.stdout.write("[INVALID] E-Mail `" + email + "` is invalid")

                    if fn and fn != "":
                        temp.first_name = fn
                    else:
                        self.stdout.write("[INVALID] First name `" + fn + "` is invalid")

                    if ln and ln != "":
                        temp.last_name = ln
                    else:
                        self.stdout.write("[INVALID] Last name `" + ln + "` is invalid")

                    if User.objects.filter(username=email).count() != 0:
                        temp = User.objects.get(username=email) # Flush all prev data and reset
                        self.stdout.write("[WARNING] username " + email + " already exists.")

                    password = User.objects.make_random_password()
                    temp.set_password(password)

                    if commit :
                        if settings.SEND_EMAIL:
                            mail.send( [temp.email], 
                                settings.DEFAULT_FROM_EMAIL, 
                                template='welcome.email',
                                context={ 
                                    'user' : temp,
                                    'password' : password,
                                    'SITE_URL' : settings.SITE_URL,
                                    'FEST_NAME' : settings.FEST_NAME,
                                },
                                headers = {},
                            )
                            # print "Error : The email id", e.user.email, "was not found. UserProfile id : ", e.id
                        temp.save()
                        temp_erp_profile, created_it = ERPProfile.objects.get_or_create(user=temp)

                    for i in core:
                        if i == "" or not i:
                            continue
                        try:
                            dept = Dept.objects.get(name__iexact = i)
                            if commit :
                                temp_erp_profile.core_relations.add(dept)
                        except Dept.DoesNotExist:
                            self.stdout.write("[INVALID] No Dept with name : " + str(i))
                        
                    for i in sc:
                        if i == "" or not i:
                            continue
                        try:
                            dept = Dept.objects.get(name__iexact = i)
                            if commit :
                                temp_erp_profile.supercoord_relations.add(dept)
                        except Dept.DoesNotExist:
                            self.stdout.write("[INVALID] No Dept with name : " + str(i))
                        
                    for i in coord:
                        if i == "" or not i:
                            continue
                        try:
                            dept = Dept.objects.get(name__iexact = i)
                            if commit :
                                temp_erp_profile.coord_relations.add(dept)
                        except Dept.DoesNotExist:
                            self.stdout.write("[INVALID] No Dept with name : " + str(i))
                        
        else :
            # No arg given - auto populate !
            pass_key = "1"
            DESC_STR = "Description for %s"
            
            for dept_name in SAMPLE_DEPTS:
                dept_name = str(dept_name).lower()

                dept, created_it = Dept.objects.get_or_create(name=dept_name)
                if created_it:
                    dept.description=DESC_STR %(dept_name)
                    dept.save()
                    self.stdout.write("Dept %s did not exist. Added it." %(dept_name))
                
                page, created_it = Page.objects.get_or_create(name=dept_name+'_page')
                page.save()

                user, created_it = User.objects.get_or_create(username=dept_name+'_core')
                user.first_name = str(dept_name).lower()
                user.last_name = "core"
                user.email = str(dept_name).lower()+'_core'+'@festapi.com'
                user.set_password(pass_key)
                user.save()
                erp_profile, created_it = ERPProfile.objects.get_or_create(user=user)
                erp_profile.core_relations.add(dept)
                
                erp_profile.save()

                subdept_name = str(dept_name) + '_subdept1'
                subdept, created_it = Subdept.objects.get_or_create(name=subdept_name, dept=dept)
                if created_it:
                    subdept.dept = dept
                    subdept.description = DESC_STR %(subdept_name)
                    subdept.save()
                    self.stdout.write("SubDept %s did not exist. Added it." %(subdept_name))
                user, created_it = User.objects.get_or_create(username=str(dept_name).lower()+'_coord1', 
                                                email=str(dept_name).lower()+'_coord1'+'@festapi.com')
                user.set_password(pass_key)
                user.first_name = str(dept_name).lower()
                user.last_name = "coord1"
                user.save()
                erp_profile, created_it = ERPProfile.objects.get_or_create(user=user)
                erp_profile.coord_relations.add(subdept)
                erp_profile.save()

                subdept_name = str(dept_name) + '_subdept2'
                subdept, created_it = Subdept.objects.get_or_create(name=subdept_name, dept=dept)
                if created_it:
                    subdept.dept = dept
                    subdept.description = DESC_STR %(subdept_name)
                    subdept.save()
                    self.stdout.write("SubDept %s did not exist. Added it." %(subdept_name))
                user, created_it = User.objects.get_or_create(username=str(dept_name).lower()+'_coord2',
                                                email=str(dept_name).lower()+'_coord2'+'@festapi.com')
                user.set_password(pass_key)
                user.first_name = str(dept_name).lower()
                user.last_name = "coord2"
                user.save()
                erp_profile, created_it = ERPProfile.objects.get_or_create(user=user)
                erp_profile.coord_relations.add(subdept)
                erp_profile.save()
                    
                self.stdout.write("Created users for Dept %s." % (dept))

            user, created_it = User.objects.get_or_create(username='root')
            user.email = "root@festapi.com"
            user.set_password(pass_key)
            user.first_name = "root"
            user.last_name = "root"
            user.save()
            erp_profile, created_it = ERPProfile.objects.get_or_create(user=user)
            for dept in Dept.objects.all():
                erp_profile.core_relations.add(dept)
                erp_profile.save()
            for subdept in Subdept.objects.all():
                erp_profile.coord_relations.add(subdept)
                erp_profile.save()
            
            self.stdout.write("Created superuser for all Depts")

            self.stdout.write("All passwords have been set to " + str(pass_key))

