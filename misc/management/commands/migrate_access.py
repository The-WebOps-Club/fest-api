from django.core.management.base import BaseCommand, CommandError, NoArgsCommand
from django.contrib.auth.models import User
from apps.users.models import Dept, Subdept, ERPProfile
from apps.walls.models import Comment, Post, Wall
from django.conf import settings
from django.template import Template,Context
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import datetime

class Command(BaseCommand):
    """
        Used to migrate existing comments and posts from v1 to v2 content-editables.
    """
    help = 'Automatically parses existing markdown based HTML'

    def handle(self, edit_all = 'true', debug = 'true',comment_end=-1, post_end=-1,**options):
        
        for p in Post.objects.all() :
            p.access_users.add(*p.notification_users.all())
            p.access_subdepts.add(*p.notification_subdepts.all())
            p.access_depts.add(*p.notification_depts.all())
            p.access_pages.add(*p.notification_pages.all())

        for w in Wall.objects.all() :
            w.access_users.add(*w.notification_users.all())
            w.access_subdepts.add(*w.notification_subdepts.all())
            w.access_depts.add(*w.notification_depts.all())
            w.access_pages.add(*w.notification_pages.all())
        
            