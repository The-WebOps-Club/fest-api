from django.core.management.base import BaseCommand, CommandError, NoArgsCommand
from django.contrib.auth.models import User
from configs import settings
from apps.users.models import Dept, Subdept, Page, ERPProfile, UserProfile
from apps.events.models import Event, EventSchedule
from apps.walls.models import Wall, Post, Comment
import json
import os
from django.conf import settings
import random
import datetime
r = lambda: random.randint(0,255)
randomcolor = lambda : '#%02X%02X%02X' % (r(),r(),r())

fn = lambda u : "" if u is None else u
fb = lambda z : "No contact information available" if z is None else "Tap on icon to call "+str(z)
from social.apps.django_app.default.models import Association, Code, Nonce, UserSocialAuth
id_markers = [
    {
        "lat": 12.989288,
        "lng": 80.237736,
        "type": "session",
        "id": "sacb",
        "title": "SAC Bowl",
        "name":"SAC Bowl"
    },
    {
        "lat": 12.989288,
        "lng": 80.237736,
        "type": "session",
        "id": "sacme",
        "title": "SAC Middle Earth",
        "name":"SAC Middle Earth"
    },
    {
        "lat": 12.99174,
        "lng": 80.232086,
        "type": "session",
        "id": "icsrh1",
        "title": "ICSR Hall 1",
        "name":"ICSR Hall 1"
    },
    {
        "lat": 12.99174,
        "lng": 80.232096,
        "type": "session",
        "id": "icsrh3",
        "title": "ICSR Hall 3",
        "name":"ICSR Hall 3"
    },
    {
        "lat": 12.99174,
        "lng": 80.232076,
        "type": "session",
        "id": "icsrma",
        "title": "ICSR Main Auditorium",
        "name":"ICSR Main Auditorium"
    },
    {
        "lat": 12.99237,
        "lng": 80.233181,
        "type": "session",
        "id": "kvgrounds",
        "title": "KV Grounds",
        "name":"KV Grounds"
    },
    {
        "lat": 12.989693,
        "lng": 80.232108,
        "type": "session",
        "id": "clt",
        "title": "CLT - Central Lecture Theatre",
        "name":"CLT"
    },
    {
        "lat": 12.99013,
        "lng": 80.232093,
        "type": "session",
        "id": "phlt",
        "title": "PhLT - Physics Lecture Theatre",
        "name":"PhLT"
    },
    {
        "lat": 12.9914963,
        "lng": 80.234608,
        "type": "session",
        "id": "doms101",
        "title": "DoMS 101 - Dept. of Management Studies",
        "name":"DoMS 101"
    },
    {
        "lat": 12.9896597,
        "lng": 80.233285,
        "type": "session",
        "id": "informals",
        "title": "Informals Zone",
        "name":"Informals Zone"
    },
    {
        "lat": 12.989386,
        "lng": 80.2372439,
        "type": "session",
        "id": "music",
        "title": "Music Park",
        "name":"Music Park"
    },
    {
        "lat": 12.9892461,
        "lng": 80.2325279,
        "type": "session",
        "id": "finearts",
        "title": "Fine Arts Hut",
        "name":"Fine Arts Hut"
    },
    {
        "lat": 12.989433,
        "lng": 80.2336504,
        "type": "session",
        "id": "midnight",
        "title": "Midnight Masters",
        "name":"Midnight Masters"
    },
    {
        "lat": 12.991769,
        "lng": 80.233430,
        "type": "session",
        "id": "adrenaline",
        "title": "Stunt Zone",
        "name":"Stunt Zone"
    },
    {
        "lat": 12.990262,
        "lng": 80.2303613,
        "type": "session",
        "id": "crc101",
        "title": "CRC 101 - Class Room Complex",
        "name":"CRC 101"
    },
    {
        "lat": 12.9900412,
        "lng": 80.2303452,
        "type": "session",
        "id": "crc102",
        "title": "CRC 102 - Class Room Complex",
        "name":"CRC 102"
    },
    {
        "lat": 12.9898628,
        "lng": 80.2303566,
        "type": "session",
        "id": "crc103",
        "title": "CRC 103 - Class Room Complex",
        "name":"CRC 103"
    },
    {
        "lat": 13.006483,
        "lng": 80.242542,
        "type": "label",
        "id": "maingate",
        "title": "Main Gate",
        "name": "Main Gate"
    },
    {
        "lat": 12.984286,
        "lng": 80.238929,
        "type": "label",
        "id": "taramani",
        "title": "Taramani Gate",
        "name": "Taramani Gate"
    },
    {
        "lat": 12.987861,
        "lng": 80.223144,
        "type": "label",
        "id": "velachery",
        "title": "Velachery Gate",
        "name": "Velachery Gate"
    },
    {
        "lat": 12.99153,
        "lng": 80.233704,
        "type": "plainsession",
        "id": "iitm",
        "title": "IIT Madras",
        "name": "IIT Madras"
    },
    {
        "lat": 12.99153,
        "lng": 80.233704,
        "type": "label",
        "id": "gc",
        "title": "GC - Gajendra Circle",
        "name": "Gajendra Circle"
    },
    {
        "lat": 12.989017,
        "lng": 80.233637,
        "type": "session",
        "id": "oat",
        "title": "OAT",
        "name": "OAT"
    },
    {
        "lat": 12.987035,
        "lng": 80.235963,
        "type": "plainsession",
        "id": "himalaya",
        "title": "Himalaya Mess",
        "name": "Himalaya"
    },
    {
        "lat": 12.991363,
        "lng": 80.234372,
        "type": "plainsession",
        "id": "kickstart",
        "title": "Kickstart Cafe",
        "name": "Kickstart Cafe"
    },
    {
        "lat": 12.986282,
        "lng": 80.234159,
        "type": "plainsession",
        "id": "sbi",
        "title": "SBI ATM",
        "name": "SBI ATM"
    },
    {
        "lat": 12.98681,
        "lng": 80.235309,
        "type": "plainsession",
        "id": "gurunath",
        "title": "Gurunath Stores",
        "name": "Gurunath Stores"
    },
    {
        "lat": 12.9916557,
        "lng": 80.2318064,
        "type": "plainsession",
        "id": "campuscafe",
        "title": "Campus Cafe",
        "name": "Campus Cafe"
    }
]
def return_room_id(venue_name):
    ret_value = ""
    for item in id_markers:
        if item["name"] == venue_name:
            ret_value = item["id"]
            break
    return ret_value
        

def return_room_location(venue_name):
    ret_value = ""
    for item in id_markers:
        if item["name"]==venue_name:
            ret_value = str(item["lat"])+","+str(item["lng"])
            break
    return ret_value

def catorder(sname):
    category_order ={ 
	'wordgames':9,    
	'classicalarts':14,
	'lecdems':13, 
	'designfest':14, 
	'westernmusic':2,
	'lightmusic':3,
	'thespian':8,  
	'writing':10, 
	'speaking':7,  
	'choreo':1,
	'designmedia':11,
	'informals':4,
	'quizzing':6,  
	'finearts':12,
	'worldfest':0,
	'lifestyle':5
    }  
    return category_order[sname]

def eventtag(cat):
    if cat == 'LECDEMS':
        return ["TAG_EVENTS", 'TAG_LECTURES', 'TOPIC_LECDEMS']
    elif cat == 'WORLDFEST':
        return ["TAG_WORLDFEST"]
    else:
        return ["TAG_EVENTS","TOPIC_"+cat]

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

        final = {}
        # JSON holding all the info
        
        final["map"] = [{
        "tiles": {
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
        },
        "config": {
            "enableMyLocation": "true"
        },
        "markers": {
            "0": id_markers 
        }
    }]
        final["blocks"]=[]
        final["partners"] = []
        final["video_library"]=[]
        final["experts"]=[]
        

        speakers_list = []
        events = Event.objects.all()
        for event in events:
            i=0
            for coord in event.coords.all():
                i+=1
                data = {
                        "name":coord.user.get_full_name(),
                        "bio":fb(coord.user.profile.mobile_number),
                        "company":"",
                        "thumbnailUrl":"https://cdn4.iconfinder.com/data/icons/social-icons-6/40/phone-48.png",
                        "id":"".join(event.name.split(" ")).lower()+"_"+str(i),
                        "plusoneUrl": fn(coord.user.profile.mobile_number)
                }
                speakers_list.append(data)
        final["speakers"] = speakers_list

        sessions_list = []
        saarang = {
            "speakers": [],
            "description":"<p>Saarang is the annual cultural festival of IIT Madras, and one of the top five best college festivals across the country. Over the years, Saarang has remained the preferred platform of an exhibition of culture, talent and competition for students from all over India, from the fields of dance, music, literature and more, all under one roof</p><p>For four days in January, IIT Madras is transformed into a hub of activity, with a large number of students, participants, and passers-by who enjoy the amalgam of events, food stalls, workshops and music shows. To the students of the institution and Chennai alike, Saarang is synonymous with culture, colour, fun, learning, and big names, big money, big dreams.</p><p>The pool of resources, great judges and opportunity it offers to young talent is a magnetic draw to students, while Chennai localites however, love Saarang for the yearly bonanza of big artistes from all over the world, performing at IIT as part of the professional and World Cultural shows. There is something for absolutely everybody, and we as we at Saarang say, this is truly the next Big Bang- see you at Saarang, for a truly out-of-the-world experience.</p>",
            "photoUrl":"http://saarang.org/mobapp_2016.jpg",
            "url": "http://saarang.org/2016/main",
            "startTimestamp": "2016-01-06T09:00:01Z",
            "endTimestamp": "2016-01-06T16:00:00Z",
            "title": "Saarang 2016",
            "youtubeUrl": "https://www.youtube.com/user/iitmsaarang",
            "mainTag": "FLAG_KEYNOTE",
            "color": randomcolor(),
            "hashtag": "saarang",
            "isLivestream": True,
            "captionsUrl": "12.9915263,80.2336853",
            "id": "__keynote__",
            "tags": ["FLAG_KEYNOTE"],
            "room": "iitm"
        }
        sessions_list.append(saarang)
        classical = {
            "speakers": [],
            "description":"<p>One of the largest Classical performances is on it's way this January with a Sarod Concert by the renowned Ustad Amjad Ali Khan and a graceful Bharatnatyam performance by the breath-taking Rukmini Vijayakumar.</p><p>Come, witness the legends perform on the star-studded opening act of Saarang 2016, the Classical Night, on 6th January at IIT Madras.</p>",
            "photoUrl":"https://scontent.fmaa1-2.fna.fbcdn.net/hphotos-xft1/v/t1.0-9/12239541_10153784749278754_8405281812068659332_n.jpg?oh=dcb7264095f49386c49e5a3861eaaf69&oe=56D5CE92",
            "url": "http://saarang.org/2016/main/proshow/classicalnight",
            "startTimestamp": "2016-01-06T12:30:00Z",
            "endTimestamp": "2016-01-06T16:30:00Z",
            "title": "Classical Night - Ustad Amjad Ali Khan and Rukmini Vijayakumar",
            "youtubeUrl": "https://www.youtube.com/user/iitmsaarang",
            "mainTag": "FLAG_KEYNOTE",
            "color": randomcolor(),
            "hashtag": "ClassicalNight",
            "isLivestream": True,
            "captionsUrl": "12.9889517,80.2336926",
            "id": "__keynote__classical__",
            "tags": ["FLAG_KEYNOTE","TAG_PROSHOWS"],
            "room": "oat"
        }
        sessions_list.append(classical)
        choreo = {
            "speakers": [],
            "description":"<p><a href='http://saarang.org/tickets?utm_source=choreo&utm_medium=android&utm_term=tickets&utm_campaign=tickets'><b>TICKETS AT BOOKMYSHOW - SAARANG</b></a></p><p>Bring the music alive, unleash yourself, dance, dance and dance till you drop. Presenting the biggest inter-collegiate dance competition, Choreo Night Saarang, IIT Madras. #JourneyOfALifetime</p>",
            "photoUrl":"https://scontent.fmaa1-2.fna.fbcdn.net/hphotos-xft1/t31.0-8/s960x960/12304288_10153786749103754_5385850861450062630_o.jpg",
            "url": "http://saarang.org/2016/main/proshow/choreonight",
            "startTimestamp": "2016-01-07T12:30:00Z",
            "endTimestamp": "2016-01-07T16:30:00Z",
            "title": "Choreo Night",
            "youtubeUrl": "https://www.youtube.com/user/iitmsaarang",
            "mainTag": "FLAG_KEYNOTE",
            "color": randomcolor(),
            "hashtag": "ChoreoNight",
            "isLivestream": True,
            "captionsUrl": "12.9889517,80.2336926",
            "id": "__keynote__choreo__",
            "tags": ["FLAG_KEYNOTE","TAG_PROSHOWS","TAG_EVENTS","TOPIC_CHOREO"],
            "room": "oat"
        }
        sessions_list.append(choreo)
        edm = {
            "speakers": [],
            "description":"<p><a href='http://saarang.org/tickets?utm_source=edm&utm_medium=android&utm_term=tickets&utm_campaign=tickets'><b>TICKETS AT BOOKMYSHOW - SAARANG</b></a></p><p>Saarang's EDM Night presents to you the electro mashup sensation - Djs From Mars as international headliners for 2016. They're bringing the party to India for the very first time, exclusively at Saarang, IIT Madras.</p><p>With mashups of popular music from all your favourite artistes, from Adele to Zedd, they have featured consistently in the range of top 100 international DJs. Known for performing with their iconic cardboard box masks, their live shows are packed with pure energy</p>",
            "photoUrl":"https://scontent.fmaa1-2.fna.fbcdn.net/hphotos-xpt1/v/t1.0-9/11221518_10153767387488754_1745811313523674850_n.jpg?oh=7d482cc4742e62a8fcfa66802089ba5a&oe=5712062A",
            "url": "http://saarang.org/2016/main/proshow/edm",
            "startTimestamp": "2016-01-08T12:30:00Z",
            "endTimestamp": "2016-01-08T16:30:00Z",
            "title": "EDM Night - DJs From MARS",
            "youtubeUrl": "https://www.youtube.com/user/iitmsaarang",
            "mainTag": "FLAG_KEYNOTE",
            "color": randomcolor(),
            "hashtag": "EDMNight",
            "isLivestream": True,
            "captionsUrl": "12.9889517,80.2336926",
            "id": "__keynote__edm__",
            "tags": ["FLAG_KEYNOTE","TAG_PROSHOWS"],
            "room": "oat"
        }
        sessions_list.append(edm)
        rockshow = {
            "speakers": [],
            "description":"<p><a href='http://saarang.org/tickets?utm_source=rockshow&utm_medium=android&utm_term=tickets&utm_campaign=tickets'><b>TICKETS AT BOOKMYSHOW - SAARANG</b></a></p><p>Saarang's Rock Show presents to you the alternative rock band - Red Jumpsuit Apparatus as headliners for 2016. They are all set to rock India for the very first time as a part of their 'Don't You Fake It 10th Anniversary World Tour' exclusively at Saarang, IIT Madras.</p><p>Known for hits such as the acoustic song - 'Your Guardian Angel', classic rock songs such as 'Face Down' and 'False Pretense' which features in the movie 'Never Back Down', they'll be performing their famous Gold Rated debut album in its entirety for the very first time since its release.</p>",
            "photoUrl":"https://scontent.fmaa1-2.fna.fbcdn.net/hphotos-xap1/v/t1.0-9/12191958_10153754315278754_5237523687656075723_n.jpg?oh=5eac512addcee33541c5c18a20f265c4&oe=571259F2",
            "url": "http://saarang.org/2016/main/proshow/rockshow",
            "startTimestamp": "2016-01-09T12:30:00Z",
            "endTimestamp": "2016-01-09T16:30:00Z",
            "title": "Rockshow - The RED JUMPSUIT Apparatus",
            "youtubeUrl": "https://www.youtube.com/user/iitmsaarang",
            "mainTag": "FLAG_KEYNOTE",
            "color": randomcolor(),
            "hashtag": "RockShow",
            "isLivestream": True,
            "captionsUrl": "12.9889517,80.2336926",
            "id": "__keynote__rockshow__",
            "tags": ["FLAG_KEYNOTE","TAG_PROSHOWS"],
            "room": "oat"
        }
        sessions_list.append(rockshow)
        popular = {
            "speakers": [],
            "description":"<p><a href='http://saarang.org/tickets?utm_source=popular&utm_medium=android&utm_term=tickets&utm_campaign=tickets'><b>TICKETS AT BOOKMYSHOW - SAARANG</b></a></p><p>Saarang's Popular Night presents to you the hit Bollywood music directing duo - Vishal & Shekhar as headliners for 2016. They are all set to energize Saarang once again with their ever so famous and award winning numbers.</p><p>Known for hits in Bollywood compositions, they have won numerous awards for their albums of the hit movies; Anjaana Anjaani, I Hate Love Storys, Jhankaar Beats, Dus, Om Shanti Om, Bachna Ae Haseeno, Dostana, Ra.One, Chennai Express, Bang Bang, Happy New Year and many more, they'll be performing from their large arsenal of reputed albums.</p>",
            "photoUrl":"https://scontent.fmaa1-2.fna.fbcdn.net/hphotos-xfa1/v/t1.0-9/12193531_10153758024703754_3346514881774312210_n.jpg?oh=4f8f1ecd83a8929c8af4d5d4ac16cfa0&oe=56D6BBA4",
            "url": "http://saarang.org/2016/main/proshow/popularnight",
            "startTimestamp": "2016-01-10T12:30:00Z",
            "endTimestamp": "2016-01-10T16:30:00Z",
            "title": "Popular Night - Vishal and Shekhar",
            "youtubeUrl": "https://www.youtube.com/user/iitmsaarang",
            "mainTag": "FLAG_KEYNOTE",
            "color": randomcolor(),
            "hashtag": "PopularNight",
            "isLivestream": True,
            "captionsUrl": "12.9889517,80.2336926",
            "id": "__keynote__popular__",
            "tags": ["FLAG_KEYNOTE","TAG_PROSHOWS"],
            "room": "oat"
        }
        sessions_list.append(popular)
        events = EventSchedule.objects.all()
        print len(events)
        tagfn = lambda u : 'TOPIC_'+u if u != 'WORLDFEST' else 'TAG_'+u
        for eventsched in events:
            color = '#%02X%02X%02X' % (r(),r(),r())
            print  str(eventsched.event.name) + " "+ fn(eventsched.comment)
            data = {
                "title": str(eventsched.event.name) + " "+ fn(eventsched.comment),
                "description": " ".join(" ".join(eventsched.event.long_description.split("\n")).split("\r")),
                "photoUrl": settings.SITE_URL + 'media/'+str(eventsched.event.event_image),
                "url": settings.MAIN_SITE + '2016/main/events/'+"".join(eventsched.event.category.lower().split(" "))+"/"+eventsched.event.name,
                "startTimestamp":eventsched.slot_start.strftime('%Y-%m-%dT%H:%M:%SZ'),
                "endTimestamp":eventsched.slot_end.strftime('%Y-%m-%dT%H:%M:%SZ'),
                "id": "_" + "".join(eventsched.event.category.split(" ")).lower()+"_"+"".join(eventsched.event.name.split(" ")).lower()+"_"+fn(eventsched.comment)+"_",
                "room":return_room_id(eventsched.venue),
                "color": color,
                "mainTag": tagfn(eventsched.event.category.upper()),
                "hashtag": eventsched.event.name,
                "isLivestream": False,
                "tags": eventtag(eventsched.event.category.upper()),
                "captionsUrl": return_room_location(eventsched.venue)
            }
            i=0
            speakers=[]
            for coord in eventsched.event.coords.all():
                i+=1
                speakers.append("".join(eventsched.event.name.split(" ")).lower()+"_"+str(i))
            data["speakers"]=speakers
            sessions_list.append(data)

        final["sessions"] = sessions_list
        print len(sessions_list) 
        rooms_list=[]
        for room in id_markers:
            rooms_list.append({"id":room["id"],"name":room["title"]})
        final["rooms"]=rooms_list
        
        tags_list = []
        data_points = ["Events","Lectures","Worldfest","Proshows"]
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
        for sname,name in categories:
            print sname, name
            if not sname=='worldfest':
                color = '#%02X%02X%02X' % (r(),r(),r())
                tags_list.append(
                    {
                        "category": "TOPIC",
                        "name": name,
                        "color": color,
                        "abstract": "",
                        "tag": "TOPIC_"+sname.upper(),
                        "original_id": "id-"+sname.lower(),
                        "order_in_category": catorder(sname)
                    } 
                )
        final["tags"] = tags_list

        vdata_file = os.path.abspath(os.path.join(data_root, "lastversion.txt"))
        manifest_file = os.path.abspath(os.path.join(data_root, "manifest.json"))

        version = 0
        with open(vdata_file, 'r') as versionfile:
            old_version = int(versionfile.readlines()[0].split(" ")[0])
            version = old_version + 1

        with open(manifest_file ,'w') as manifest_out:
            manifest_data = {
               "format": "iosched-json-v1",
                "data_files": [
                    "android_v"+str(version)+".json"
                ] 
            }
            json.dump(manifest_data, manifest_out)
            
        android_file = os.path.abspath(os.path.join(data_root, "android_v"+str(version)+".json"))
        with open(android_file, 'w') as outfile:
            json.dump(final, outfile)
        self.stdout.write("User ... done.")

        self.stdout.write("Dept > Users + Subdepts > Users ... done.")

        with open(vdata_file, 'w') as versionfile:
            versionfile.write(str(version))

        self.stdout.write("All done")

