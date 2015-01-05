from django.core.management.base import BaseCommand, CommandError, NoArgsCommand
from django.contrib.auth.models import User
from configs import settings
import json
import os
from django.conf import settings
import re
from apps.users.models import UserProfile
from post_office import mail
EMAIL_REGEX = re.compile(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$")
import time
def chunkify(lst,n):
    return [ lst[i::n] for i in xrange(n) ]
class Command(BaseCommand):
    """
        Send email 
    """
    help = 'Send email with the given template'

    def handle(self, *args, **options):
        members = User.objects.all()
        #email_list=[]
        #for user in members:
        #    email_id = user.user.email
        #    if EMAIL_REGEX.match(email_id):
        #        email_list.append(email_id)
        #print "Sending emails to ", len(email_list), "users "
        #unsubscribe_link = "dasdasdasei8rwer9f898fasd89a"
        #email_list = ['muhammedshahid.k@gmail.com']
        #mail.send(
        #    sender = settings.DEFAULT_MAIN_FROM_EMAIL,
        #    bcc = email_list,
        #    template = args[0],
        #    context = {'FEST_NAME': settings.FEST_NAME, 'SITE_URL': settings.SITE_URL, 'unsubscribe_link': unsubscribe_link},
        #    headers = {'List-Unsubscribe': unsubscribe_link}
        #) 
        user_list = [] 
        email_list =[]
        unsubscribe_link = "dasdasdasei8rwer9f898fasd89a"
        for user in members:
            print "Verifying ",user.email
            email_id = user.email
            if EMAIL_REGEX.match(email_id):
                user_list.append(user)
        #user_list = [User.objects.get(email="muhammedshahid.k@gmail.com")]
        for user in user_list:
            email = {
                'sender': settings.DEFAULT_MAIN_FROM_EMAIL,
                'recipients':  [str(user.email)],
                'template':args[0],
                'context' : {'user':user, 'FEST_NAME': settings.FEST_NAME, 'SITE_URL': settings.SITE_URL, 'unsubscribe_link': unsubscribe_link},
                'headers' :{'List-Unsubscribe': unsubscribe_link}
            }
            print 'processed', user.email
            email_list.append(email)
        print "finised processing"
        split_list = chunkify(email_list,10) 
        i=0
        for part in split_list:
            i+=1
            mail.send_many(part)
            time.sleep(5)
            print "Sending part ",i
        print "Sending emails to ", len(email_list), "users "
        self.stdout.write("All done")

