from django.core.management.base import BaseCommand, CommandError, NoArgsCommand
from django.contrib.auth.models import User
from apps.users.models import Dept, Subdept, ERPProfile
from apps.walls.models import Wall, Post, Comment

class Command(BaseCommand):
    """
        Give all users access rights to everyone
    """
    help = 'Automatically adds required entries into the database. esp Departments and Walls for them.'

    def handle(self, arg=None, **options):

        total = Wall.objects.count()

        for w in Wall.objects.all():
            w_parent = w.parent
            w.add_notifications([w_parent])
            print "Done : ", count, "of", total

        self.stdout.write("Everyone can access everything.")

