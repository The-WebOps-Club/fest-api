from django.core.management.base import BaseCommand, CommandError, NoArgsCommand
from django.contrib.auth.models import User
from apps.users.models import Dept, Subdept, ERPProfile
from apps.walls.models import Comment, Post
from notifications.models import Notification
from django.conf import settings
from django.template import Template,Context
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import datetime

class Command(BaseCommand):
    """
        Used to migrate existing notifications from v1 to v2 (supports unread_by_wall).
    """
    help = 'Automatically parses existing markdown based HTML'

    def handle(self, debug = 'true' ,**options):
        for c in Notification.objects.all():
            c.description = 'wall:'+format(c.target.wall.id)
            c.save();
            if debug:
                print('migrated '+format(c.pk))

