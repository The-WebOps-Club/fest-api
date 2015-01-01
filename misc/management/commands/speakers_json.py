from django.core.management.base import BaseCommand, CommandError, NoArgsCommand
from django.contrib.auth.models import User
from configs import settings
from apps.users.models import Dept, Subdept, Page, ERPProfile, UserProfile
from apps.events.models import Event
from apps.walls.models import Wall, Post, Comment
import json
import os

from social.apps.django_app.default.models import Association, Code, Nonce, UserSocialAuth

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
        speakers_list = []
        events = Event.objects.all()
        for event in events:
            i=0
            for coord in event.coords.all():
                try:
                    fb_id = UserSocialAuth.objects.get(user=coord.user,provider="facebook").uid
                    thumb = "http://graph.facebook.com/"+str(fb_id)+"/picture?height=60&width=60"
                except:
                    thumb = "https://cdn3.iconfinder.com/data/icons/iconka-buddy-set/64/astronaut_64.png"
                    
                i+=1
                data = {
                        "name":coord.user.get_full_name(),
                        "bio":"<details>",
                        "company":"",
                        "thumbnailUrl":thumb,
                        "id":"".join(event.name.split(" ")).lower()+"_"+str(i),
                        "plusoneUrl":coord.user.profile.mobile_number
                }
                speakers_list.append(data)
        final["speakers"] = speakers_list
        android_file = os.path.abspath(os.path.join(data_root, "speakers.json"))

        with open(android_file, 'w') as outfile:
            json.dump(final, outfile)
        self.stdout.write("User ... done.")

        self.stdout.write("Dept > Users + Subdepts > Users ... done.")

        self.stdout.write("All done")

