from django.core.management.base import BaseCommand, CommandError, NoArgsCommand
from django.contrib.auth.models import User
from configs import settings
from apps.users.models import Dept, Subdept, Page, ERPProfile, UserProfile
from apps.events.models import Event
from apps.walls.models import Wall, Post, Comment
import json
import os

class Command(BaseCommand):
    """
        Generate the JSON for Google IO android app    
    """
    help = 'Generate the JSON required by Saarang Android app Speakers'

    def handle(self, arg=None, **options):

        static_files = settings.STATICFILES_DIRS[0]
        data_root = os.path.abspath(os.path.join(static_files, "json"))
        
        if not os.path.exists(data_root):
            os.makedirs(data_root)

        final = {}
        # JSON holding all the info
        ''' 
        # Create other JSONs part by part
        # Map
        map_json = {}
        map_json["tiles"] = {
          "0": {
            "url": "",
            "filename": "floor0-2014-v1.svg"
          },
          "1": {
            "url": "",
            "filename": "floor0-2014-v1.svg"
          },
          "2": {
            "url": "",
            "filename": "floor0-2014-v1.svg"
          }
        }
        map_json["config"] = {
          "enableMyLocation": "true"
        }
        
        map_json["markers"] = {
            "0": [
            {
                "lat": 12.989288,
                "lng": 80.237736,
                "type": "session",
                "id": "sacb",
                "title": "SAC Bowl"
            },
            {
                "lat": 12.989288,
                "lng": 80.237736,
                "type": "session",
                "id": "sacme",
                "title": "SAC Middle Earth"
            },
            {
                "lat": 12.989288,
                "lng": 80.237736,
                "type": "session",
                "id": "sac",
                "title": "SAC"
            },
            {
                "lat": 12.991740,
                "lng": 80.232086,
                "type": "session",
                "id": "icsrma",
                "title": "ICSR Main Auditorium"
            },
            {
                "lat": 12.991740,
                "lng": 80.232086,
                "type": "session",
                "id": "icsrh1",
                "title": "ICSR Hall 1"
            },
            {
                "lat": 12.992370,
                "lng": 80.233181,
                "type": "session",
                "id": "kvgrounds",
                "title": "KV Grounds"
            },
            {
                "lat": 12.989693,
                "lng": 80.232108,
                "type": "session",
                "id": "clt",
                "title": "CLT"
            },
            {
                "lat": 12.990645,
                "lng": 80.230815,
                "type": "session",
                "id": "mechdept",
                "title": "MSB"
            },
            {
                "lat": 13.006483,
                "lng": 80.242542,
                "type": "label",
                "id": "maingate",
                "title": "Main Gate"
            },
            {
                "lat": 12.984286,
                "lng": 80.238929,
                "type": "label",
                "id": "taramani",
                "title": "Taramani Gate"
            },
            {
                "lat": 12.987861,
                "lng": 80.223144,
                "type": "label",
                "id": "velachery",
                "title": "Velachery Gate"
            },
            {
                "lat": 12.991530,
                "lng": 80.233704,
                "type": "label",
                "id": "gc",
                "title": "Gajendra Circle"
            },
            {
                "lat": 12.989017,
                "lng": 80.233637,
                "type": "plainsession",
                "id": "oat",
                "title": "OAT"
            },
            {
                "lat": 12.987035,
                "lng": 80.235963,
                "type": "plainsession",
                "id": "himalaya",
                "title": "Himalaya"
            },
            {
                "lat": 12.991363,
                "lng": 80.234372,
                "type": "plainsession",
                "id": "kickstart",
                "title": "Kickstart Cafe"
            },
            {
                "lat": 12.986282,
                "lng": 80.234159,
                "type": "plainsession",
                "id": "sbi",
                "title": "SBI ATM"
            },
            {
                "lat": 12.986810,
                "lng": 80.235309,
                "type": "plainsession",
                "id": "gurunath",
                "title": "Gurunath Stores"
            }
            ]} 
        '''
        speakers_list = []
        events = Event.objects.all()
        for event in events:
            i=0
            for coord in event.coords.all():
                i+=1
                data = {
                        "name":coord.user.get_full_name(),
                        "bio":"",
                        "company":"",
                        "plusoneUrl": "",
                        "thumbnailUrl":"",
                        "id":"".join(event.name.split(" ")).lower()+"_"+str(i),
                        "mobile":coord.user.profile.mobile_number
                }
                print data
                speakers_list.append(data)
        final["speakers"] = speakers_list
        android_file = os.path.abspath(os.path.join(data_root, "speakers.json"))

        with open(android_file, 'w') as outfile:
            json.dump(final, outfile)
        self.stdout.write("User ... done.")

        self.stdout.write("Dept > Users + Subdepts > Users ... done.")

        self.stdout.write("All done")

