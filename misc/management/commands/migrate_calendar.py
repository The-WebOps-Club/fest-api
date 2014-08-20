from django.core.management.base import BaseCommand, CommandError, NoArgsCommand
from django.contrib.auth.models import User
from apps.users.models import Dept, Subdept, ERPProfile, Page
from apps.walls.models import Comment, Post
from django.conf import settings
from django.template import Template,Context
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from apps.portals.general.utils import attach_drive_to_entity, share_drive, attach_calendar_to_entity, share_calendar
import datetime
from apps.docs.utils import Drive,Calendar

import time

class Command(BaseCommand):
    """
        Used to migrate existing subdepts and depts to a newer calendar-linked version.
    """
    help = 'Attaches calendars to depts and subdepts and shares them with the concerned people'

    def handle(self,  **options):

        calendar = Calendar()

        entity_set = list(Dept.objects.all()) + list(Page.objects.all())

        for entity in entity_set:
            time.sleep(1)
            print "executing ", entity.name
            if not entity.calendar_id:
                attach_calendar_to_entity( calendar, entity )
            share_calendar( calendar, entity )