from django.core.management.base import BaseCommand, CommandError, NoArgsCommand
from django.contrib.auth.models import User
from configs import settings
from apps.users.models import Dept, Subdept, Page, ERPProfile, UserProfile
from apps.events.models import Event
from apps.walls.models import Wall, Post, Comment
import json
import os
from django.conf import settings
import random
r = lambda: random.randint(0,255)

class Command(BaseCommand):
    """
        Generate the JSON for Google IO android app    
    """
    help = 'Generate the JSON required by Saarang Android app Tags'

    def handle(self, arg=None, **options):

        static_files = settings.STATICFILES_DIRS[0]
        data_root = os.path.abspath(os.path.join(static_files, "json"))
        
        if not os.path.exists(data_root):
            os.makedirs(data_root)

        final = {}
        # JSON holding all the info
        tags_list = []
        data_points = ["Events","Workshops","Lectures","Exhibition"]
        i=0
        for data in data_points:
            i+=1
            tags_list.append(
                {
                    "category": "THEME",
                    "name": data,
                    "abstract": "",
                    "tag": "TAG_"+data.upper(),
                    "original_id": "id-"+data.lower(),
                    "order_in_category": i
                }
            )
        categories = settings.EVENT_CATEGORIES
        j=0
        for sname,name in categories:
            print sname, name
            j+=1
            color = '#%02X%02X%02X' % (r(),r(),r())
            tags_list.append(
                {
                    "category": "TOPIC",
                    "name": name,
                    "color": color,
                    "abstract": "",
                    "tag": "TOPIC_"+sname.upper(),
                    "original_id": "id-"+sname.lower(),
                    "order_in_category": j
                } 
            )
        final["tags"] = tags_list
        android_file = os.path.abspath(os.path.join(data_root, "tags.json"))

        with open(android_file, 'w') as outfile:
            json.dump(final, outfile)
        self.stdout.write("User ... done.")

        self.stdout.write("Dept > Users + Subdepts > Users ... done.")

        self.stdout.write("All done")

