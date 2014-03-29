from django.core.management.base import BaseCommand, CommandError, NoArgsCommand
from django.contrib.auth.models import User
from apps.walls import Wall
from apps.users import Department

class Command(BaseCommand):
    """
    """
    help = ''

    def handle(self, arg=None, **options):
        depts = Department.objects.all()
        # for dept in depts:
        #     profiles = ERPProfile.objects.filter(core_relation__name=dept.name)
        #     