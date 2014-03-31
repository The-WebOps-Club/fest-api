from django.core.management.base import BaseCommand, CommandError, NoArgsCommand
from django.contrib.auth.models import User
from apps.users.models import Dept, Subdept, ERPProfile

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

DESC_STR = "Description for %s"

class Command(BaseCommand):
    """
        Creates the department given in SAMPLE_DEPTS and add a core
        and two coordinators to the users for each dept.

        dept_core, dept_coord1 and dept_coord2

        Password is 'password' for all the users
    """
    help = 'Automatically adds required entries into the database. esp Departments and Walls for them.'

    def handle(self, arg=None, **options):
        # Department specific users
        pass_key = "1"
        
        for dept_name in SAMPLE_DEPTS:
            dept_name = str(dept_name).lower()

            dept, created_it = Dept.objects.get_or_create(name=dept_name)
            if created_it:
                dept.description=DESC_STR %(dept_name)
                dept.save()
                self.stdout.write("Dept %s did not exist. Added it." %(dept_name))
                
            user, created_it = User.objects.get_or_create(username=dept_name+'_core', 
                                            email=str(dept_name).lower()+'_core'+'@festapi.com')
            user.first_name = str(dept_name).lower()
            user.last_name = "core"
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