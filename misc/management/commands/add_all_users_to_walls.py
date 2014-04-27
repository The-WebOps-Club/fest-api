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

        total = Wall.objects.count() + Post.objects.count()
        users = User.objects.all()
        for w in Wall.objects.all():
            for u in users:
                t = []
                t.extend(u.core_relations)
                t.extend(u.supercoord_relations)
                t.extend(u.coord_relations)
                for u_rel in t:
                    if u_rel.wall == w:
                        w.notification_users.add(u)

            w.owners.add(*User.objects.all())
            w.visible_to.add(*User.objects.all())
            count += 1
            print "Done : ", count, "of", total

        for p in Post.objects.all():
            for u in users:
                t = []
                t.extend(u.core_relations)
                t.extend(u.supercoord_relations)
                t.extend(u.coord_relations)
                for u_rel in t:
                    if u_rel.wall == p.wall:
                        w.notification_users.add(u)
            p.visible_to.add(*User.objects.all())
            p.is_public = True
            count += 1
            print "Done : ", count, "of", total
            
        self.stdout.write("Everyone can access everything.")

