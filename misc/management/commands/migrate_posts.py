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

    def handle(self, edit_all = 'false', debug = 'true',comment_end=-1, post_end=-1,**options):
        for c in Comment.objects.all() :
            if edit_all or ( comment_end != -1 and c.pk < comment_end) :
                try:
                    rendered_comment = Template('{%load markdown_tags%}{%autoescape off%}{{comment_text|markdown}}{%endautoescape%}').render(Context({'comment_text':c.description}))
                    c.description = rendered_comment
                    if debug:
                        print "Parsed: "+format(c.pk)
                except Exception as e:
                    if debug:
                        print(e.message)
                    

                c.save();

        for c in Post.objects.all() :
            if edit_all or ( post_end != -1 and c.pk < pk_end) :
                try:
                    rendered_comment = Template('{%load markdown_tags%}{%autoescape off%}{{post_text|markdown}}{%endautoescape%}').render(Context({'post_text':c.description}))
                    c.description = rendered_comment
                except Exception as e:
                    if debug:
                        print(e.message);

                c.save();

