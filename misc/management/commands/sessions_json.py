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
    help = 'Generate the JSON required by Saarang Android app Sessions'

    def handle(self, arg=None, **options):

        static_files = settings.STATICFILES_DIRS[0]
        data_root = os.path.abspath(os.path.join(static_files, "json"))
        
        if not os.path.exists(data_root):
            os.makedirs(data_root)

        final = {}
        # JSON holding all the info
        sessions_list = []
        events = Event.objects.all()
        for event in events:
            color = '#%02X%02X%02X' % (r(),r(),r())
            data = {
                "title": event.name,
                "description": " ".join(" ".join(event.long_description.split("\n")).split("\r")),
                "photoUrl": settings.SITE_URL + 'media/'+str(event.event_image),
                "url": settings.MAIN_SITE + '2015/main/events/'+"".join(event.category.lower().split(" "))+"/"+event.name,
                "startTimestamp":"",
                "endTimestamp":"",
                "id": "".join(event.category.split(" ")).lower()+"_"+"".join(event.name.split(" ")).lower(),
                "room":"",
                "color": color
            }
            i=0
            speakers=[]
            for coord in event.coords.all():
                i+=1
                speakers.append("".join(event.name.split(" ")).lower()+"_"+str(i))
            data["speakers"]=speakers
            sessions_list.append(data)

        final["sessions"] = sessions_list
        android_file = os.path.abspath(os.path.join(data_root, "sessions.json"))

        with open(android_file, 'w') as outfile:
            json.dump(final, outfile)
        self.stdout.write("User ... done.")

        self.stdout.write("Dept > Users + Subdepts > Users ... done.")

        self.stdout.write("All done")

