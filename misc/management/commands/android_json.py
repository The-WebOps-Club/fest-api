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
            "photoUrl":"http://saarang.org/mobapp.jpg",
            "url": "http://saarang.org/2015/main",
            "startTimestamp": "2015-01-07T09:00:01Z",
            "endTimestamp": "2015-01-07T16:00:00Z",
            "title": "Saarang 2015",
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
            "description":"<p>Saarang IIT Madras presents two of the leading lights in the field of classical dance and music. Two women who have revolutionized the performing arts with their versatility and energy will grace the Open Air Theatre this January. Be there to see Padma Shri Aruna Sairam and Padma Shri Shobana enthral you.</p><p>Padma Shri Shobana Chandrakumar is an Indian film actress and Bharata Natyam dancer. Shobana was trained under the Bharata Natyam dancers Chitra Visweswaran and Padma Subrahmanyam. She emerged as an independent performer and choreographer in her twenties. Shobana danced Abhinaya, a pivotal element in Bharata Natyam. She has worked on collaborative ventures with the likes of tabla maestro Zakir Hussain, Vikku Vinayakram and Mandolin Srinivas. Her recitals abroad include those at the World Malayalee convention, United States, in Kuala Lumpur before the King and Queen of Malaysia and numerous other places. In 2006, the Indian Government honoured Shobana with the Padma Shri for her contributions towards the classical dance. In 2014, The Kerala Government honoured her with the Kala Ratna Award.</p><p>Padma Shri Aruna Sairam is an eminent Carnatic music vocalist. In concert she continually strives to deliver a unique experience through new repertoire. Aruna has had the rare distinction of performing in such venues as the Rashtrapati Bhavan, Shakthi Sthal and Vir Bhoomi. Aruna is one of her generation's pioneering vocalists in the sense of sensitising international audiences to the sound and feel of South Indian vocal music. The BBC Proms invited her to perform at London's Royal Albert Hall as the first South Indian classical vocalist in the Proms' history. Aruna has also performed at New York's Carnegie Hall, Theatre de la Ville in Paris and Morocco's Fes Festival of World Sacred Music. The awards with which she was honoured are Padma Shri from the Government of India and the Sangeet Natak Akademi Award, Government of India in 2014. Aruna Sairam has been appointed the Advisor to the Department of Culture, Tamil Nadu, on Musical Education by the Chief Minister of Tamil Nadu.</p><p>Come, witness these stalwarts of Indian Classical Arts inaugurate Saarang 2015 on the star-studded opening night. Entry is free for all.</p>",
            "photoUrl": "https://scontent-b-hkg.xx.fbcdn.net/hphotos-xap1/t31.0-8/10633931_10152894895288754_832279855549353651_o.jpg",
            "url": "http://saarang.org/2015/main/proshow/classicalnight",
            "startTimestamp": "2015-01-07T18:00:00Z",
            "endTimestamp": "2015-01-07T22:00:00Z",
            "title": "Classical Night - Shobana and Aruna Sairam",
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
            "description":"<p><a href='http://saarang.org/tickets'><b>TICKETS AT BOOKMYSHOW - SAARANG</b></a></p><p>Bring the music alive, unleash yourself, dance, dance and dance till you drop. Presenting the biggest inter-collegiate dance competition, Choreo Night Saarang, IIT Madras. #NextBigBang</p>",
            "photoUrl": "https://fbcdn-sphotos-e-a.akamaihd.net/hphotos-ak-xpa1/v/t1.0-9/p417x417/10665860_10152870151618754_6329641390005030213_n.jpg?oh=4b4a4bce6fdc1d8ecfd23438b131568c&oe=55455147&__gda__=1429213880_b05dae093461879471d34c7d45035698",
            "url": "http://saarang.org/2015/main/proshow/choreonight",
            "startTimestamp": "2015-01-08T18:00:00Z",
            "endTimestamp": "2015-01-08T22:00:00Z",
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
            "description":"<p><a href='http://saarang.org/tickets'><b>TICKETS AT BOOKMYSHOW - SAARANG</b></a></p><p>IIT Madras gives you the headlining acts for the Vh1 Supersonic 101 EDM Night at Saarang 2015 to be held on January 9th, 2015 at the OAT.</p><p><b>Nucleya</b></p><p>He's back to perform at Saarang, bigger and with a whole new bunch of bells and whistles in his arsenal. One simply cannot resist partying when he drops those Desi beats. Till date, he remains the biggest phenomenon of Dubstep in the country. He has 14 singles, studio albums and collaborations to his name and has performed at numerous music festivals around the world.</p><p><b>Thermal Projekt</b></p><p>Their passion and love for music, bonds their personalities together. Known for winning hearts with their smashing remixes, mashups and originals earned the duo their massive popularity on Facebook and Twitter. They have often shared the stage with international greats. Most recently, they opened for Dada Life Concert in Bangalore.</p><p><b>Progressive Brothers</b></p><p>Their style and identity comprises of 'Big room' Progressive House and melodies of Trance Music with the trace of Electro in it. Their debut track 'Veda' was in collaboration with Trance legend 'Richard Durand'. They have also featured on compilations 'Trance-Central 003', 'Amsterdam Dance Essentials' and 'Heaven Trance' along with some Top DJs from DJ Mag Top 100 such as Cosmic Gate and Stoneface.</p><p>EDM Night, the latest addition to the pro-shows, has taken Saarang by storm and promises to be a spectacle worth experiencing!</p>",
            "photoUrl": "https://scontent-a-hkg.xx.fbcdn.net/hphotos-xpa1/v/t1.0-9/p417x417/10407724_10152845895118754_8546661407146452245_n.jpg?oh=9784464e67088ea3cd7aaa28658c27b0&oe=54FBAC1C",
            "url": "http://saarang.org/2015/main/proshow/edm",
            "startTimestamp": "2015-01-09T18:00:00Z",
            "endTimestamp": "2015-01-09T22:00:00Z",
            "title": "EDM Night - Thermal Projekt, Nucleya, Progressive Brothers",
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
            "description":"<p><a href='http://saarang.org/tickets'><b>TICKETS AT BOOKMYSHOW - SAARANG</b></a></p><p>IIT Madras is proud to announce Karnivool as the headlining act for the Rock Show at Saarang 2015. Karnivool will be performing live for the first time in Chennai, at the IIT Madras Open Air Theatre on January 10th, 2015.</p><p>Karnivool is an Australian progressive rock band from Perth, Australia, critically hailed as being one of the bands that established the Australian progressive rock and metal movement. They are considered to be amongst the few in Australia's rapidly growing music industry to still be bringing new and refreshing material to their catalogue. The five-member band consists of Ian Kenny on vocals, Drew Goddard and Mark Hosking on guitar, Jon Stockman on bass, and Steve Judd on drums.</p>",
            "photoUrl": "https://fbcdn-sphotos-a-a.akamaihd.net/hphotos-ak-xpa1/t31.0-8/s960x960/10629424_10152813251613754_955379862189032201_o.jpg",
            "url": "http://saarang.org/2015/main/proshow/rockshow",
            "startTimestamp": "2015-01-10T18:00:00Z",
            "endTimestamp": "2015-01-10T22:00:00Z",
            "title": "Rockshow - Karnivool",
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
            "description":"<p><a href='http://saarang.org/tickets'><b>TICKETS AT BOOKMYSHOW - SAARANG</b></a></p><p>Saarang 2015 presents the scintillating Sunidhi Chauhan performing live at Popular Night. She is set to perform at the OAT IIT Madras on January 11th 2015.</p><p>Sunidhi Chauhan is one of the most popular Indian playback singers and performers today. Her main claim to fame is her active role in the Bollywood music industry. With 1000s of studio recordings over a few years she rapidly became one of India's most recorded voices and a popular name. She has also recorded songs in several other dialects and languages, such as Punjabi, Marathi, Kannada, Tamil, Telugu, Malayalam, Bengali and English. She has been awarded with prestigious national awards on several occasions and has established herself as the strongest live performer and singer in India to date. Sunidhi Chauhan made her International debut with the song Heartbeat, a collaboration with Enrique Iglesias. Sunidhi stepped into the world of playback singing with the 1996 Bollywood film, Shastra, lending her voice to the song 'Larki Deewaani Dekho, Ladka Deewaana.' By the age of nineteen, Sunidhi had lent her voice to over 350 songs. With blockbuster hits like 'Dance pe Chance', 'Sheila ki Jawani', 'Aaja Nachle' and 'Crazy Kiya Re' her voice has defined Bollywood music over the past decade.</p><p>Sunidhi is one of the most decorated Indian singers with 54 nominations for best playback singer. Having won the 'Best Playback Singer' award from Filmfare, International Indian Film Academy, Star Screen, GIMA and several others 20 times, she is undoubtedly the most gifted Bollywood playback singer of the present era. Legendary playback singer Lata Mangeshkar described Sunidhi as the 'numero uno' female singer of today while Shankar Mahadevan referred to her as the 'Best female singer and live performer today.'With greats such as Sonu Nigam, Vishal-Shekhar, Shankar-Ehsaan-Loy, Salim-Sulaiman having rocked the OAT at IIT Madras in the past, one expects an exciting performance at Popular Night each year. Sunidhi Chauhan is set raise the bar further this year with a plethora of songs which are bound to keep the crowd on their feet all night long.</p><p>We missed the 'first big bang', let's not miss the 'next one' at Saarang 2015!</p>",
            "photoUrl": "https://scontent-a-hkg.xx.fbcdn.net/hphotos-xfa1/v/t1.0-9/p417x417/1743464_10152841504773754_6092583807272369215_n.jpg?oh=a0f6149b8b6e214daf5adacf8baa388e&oe=55428DCD",
            "url": "http://saarang.org/2015/main/proshow/popularnight",
            "startTimestamp": "2015-01-11T18:00:00Z",
            "endTimestamp": "2015-01-11T22:00:00Z",
            "title": "Popular Night - Sunidhi Chauhan",
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
                "url": settings.MAIN_SITE + '2015/main/events/'+"".join(eventsched.event.category.lower().split(" "))+"/"+eventsched.event.name,
                "startTimestamp":(eventsched.slot_start+datetime.timedelta(hours=5,minutes=30)).strftime('%Y-%m-%dT%H:%M:%SZ'),
                "endTimestamp":(eventsched.slot_end+datetime.timedelta(hours=5,minutes=30)).strftime('%Y-%m-%dT%H:%M:%SZ'),
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

