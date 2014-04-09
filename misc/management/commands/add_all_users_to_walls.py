from django.core.management.base import BaseCommand, CommandError, NoArgsCommand
from django.contrib.auth.models import User
from apps.users.models import Dept, Subdept, ERPProfile
from apps.walls.models import Wall, Post, Comment

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
        Give all users access rights to everyone
    """
    help = 'Automatically adds required entries into the database. esp Departments and Walls for them.'

    def handle(self, arg=None, **options):

        for w in Wall.objects.all():
            w.notification_users.add(*User.objects.all())
            w.owners.add(*User.objects.all())
            w.visible_to.add(*User.objects.all())

        for p in Post.objects.all():
            p.notification_users.add(*User.objects.all())
            p.visible_to.add(*User.objects.all())
            p.is_public = True
        self.stdout.write("Everyone can access everything.")

