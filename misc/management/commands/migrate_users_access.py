from django.core.management.base import BaseCommand, CommandError, NoArgsCommand
from django.contrib.auth.models import User
from apps.users.models import Dept, Subdept, ERPProfile
from apps.walls.models import Comment, Post
from django.conf import settings
from django.template import Template,Context
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from annoying.functions import get_object_or_None
from django.contrib.auth.models import User
from configs import settings
from apps.users.models import Dept, Subdept, ERPProfile
from apps.walls.models import Wall, Post, Comment
from django.template import RequestContext
from django.template.loader import render_to_string

from apps.walls.utils import get_tag_object
from annoying.functions import get_object_or_None
# Decorators
from django.contrib.auth.decorators import login_required, user_passes_test
#from apps.users.models.ERPProfile import populate
import json

import datetime
class Command(BaseCommand):
    """
        Used to migrate existing comments and posts from v1 to v2 content-editables.
    """
    help = 'Automatically parses existing markdown based HTML'

    def handle(self,  **options):

        for post in Post.objects.all():

            try:
                obj = get_object_or_None(User, id=int(id))
                if isinstance(obj, User):
                 obj_profile = obj.profile
                 obj_erp_profile = obj.erp_profile
	         populate_func1=populate(obj_erp_profile)
                 
                if(hasattr(post.wall,'person')):
                    post.access_specifier = 1
                else:
                    post.access_specifier = 2
                post.save()
            except Exception as e:
                print(e.message);
