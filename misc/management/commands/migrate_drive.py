from django.core.management.base import BaseCommand, CommandError, NoArgsCommand
from django.contrib.auth.models import User
from apps.users.models import Dept, Subdept, ERPProfile
from apps.walls.models import Comment, Post
from django.conf import settings
from django.template import Template,Context
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from apps.portals.general.utils import attach_drive_to_entity, share_drive
import datetime

class Command(BaseCommand):
    """
        Used to migrate existing subdepts and depts to a newer drive-linked version.
    """
    help = 'Attaches drive folders to depts and subdepts and shares them with the concerned people'

    def handle(self,  **options):

        drive = Drive()

        entity_set = list(Dept.objects.all()) + list(Subdept.objects.all()) + list(Page.objects.all())

        for entity in entity_set:
            attach_drive_to_entity( drive, entity )
            share_drive( drive, entity )