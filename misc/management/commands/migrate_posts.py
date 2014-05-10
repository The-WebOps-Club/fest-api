from django.core.management.base import BaseCommand, CommandError, NoArgsCommand
from django.contrib.auth.models import User
from apps.users.models import Dept, Subdept, ERPProfile
from django.conf import settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import datetime

class Command(BaseCommand):
    """
        Used to migrate existing comments and posts from v1 to v2 content-editables.
    """
    help = 'Automatically parses existing markdown based HTML'

    def handle(self, pk_end,**options):
        for c in Comment.objects.all():
            if c.pk < pk_end:
                rendered_comment = Template('{%load markdown_tags%}{%autoescape off%}{{comment_text|markdown}}{%endautoescape%}').render(RequestContext({'comment_text':c.description}))
                c.description = rendered_comment
                c.save();

