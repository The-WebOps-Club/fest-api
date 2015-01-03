from django.core.management.base import BaseCommand, CommandError, NoArgsCommand
from django.contrib.auth.models import User
from configs import settings
from apps.users.models import Dept, Subdept, Page, ERPProfile, UserProfile
from apps.events.models import Event, EventSchedule, WebsiteUpdate
from apps.walls.models import Wall, Post, Comment
import json
import os
from django.conf import settings
import random
import datetime

class Command(BaseCommand):
    """
        Generate the JSON for Google IO android app    
    """
    help = 'Generate the JSON required by Saarang Android app All'

    def handle(self, arg=None, **options):

        static_files = settings.STATICFILES_DIRS[0]
        data_root = os.path.abspath(os.path.join(static_files, "json"))
        
        if not os.path.exists(data_root):
            os.makedirs(data_root)

        final = []
        # JSON holding all the info
        updates = WebsiteUpdate.objects.all()
        for update in updates:
            data = {
                "type": update.type,
                "title": update.title,
                "text": update.text
            }
            final.append(data)
        updates_file = os.path.abspath(os.path.join(data_root, "updates.json"))
        with open(updates_file, 'w') as outfile:
            json.dump(final, outfile)


        self.stdout.write("All done")

