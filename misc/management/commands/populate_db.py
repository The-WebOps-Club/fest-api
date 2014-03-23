from django.core.management.base import BaseCommand, CommandError, NoArgsCommand
from django.contrib.auth.models import User
from apps.users.models import Dept, Subdept, ERPUser

SAMPLE_DEPTS = [
    'Events',
    'Design',
    'Facilities',
    'Finance',
    'Hospitality',
    'Publicity',
    'QMS',
    'Sponsorship'
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
        for dept in SAMPLE_DEPTS:
            try:
                Dept.objects.get(name=dept)
                self.stdout.write("Dept %s already exists. Not changing anything." %(dept))
            except Dept.DoesNotExist:
                self.stdout.write("Dept %s does not exist. Adding entries." %(dept))
                new_dept = Dept.objects.create(name=dept, description=DESC_STR %(dept))
                new_user = User.objects.create_user(username=dept.lower()+'_core', password='password', email=dept.lower()+'_core'+'@festapi.com')
                profile = ERPUser.objects.create(user=new_user)
                profile.core_relations.add(new_dept)
                profile.save()
                new_user = User.objects.create_user(username=dept.lower()+'_coord1', password='password', email=dept.lower()+'_coord1'+'@festapi.com')
                profile = ERPUser.objects.create(user=new_user)
                new_user = User.objects.create_user(username=dept.lower()+'_coord2', password='password', email=dept.lower()+'_coord2'+'@festapi.com')
                profile = ERPUser.objects.create(user=new_user)
                self.stdout.write("Dept %s entries completed." % (dept))