from django.core.management.base import BaseCommand, CommandError, NoArgsCommand
from django.contrib.auth.models import User
from apps.users.models import Dept, Subdept, ERPProfile
from apps.walls.models import Comment, Post
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

    def handle(self, level = 1, **options):

        for post in Post.objects.all() :
            try:
                post.access_specifier = level
                post.save()
            except Exception as e:
                if debug:
                    print(e.message);
