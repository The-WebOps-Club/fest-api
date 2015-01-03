from django.core.management.base import BaseCommand, CommandError, NoArgsCommand
from django.contrib.auth.models import User
from configs import settings
import json
import os
from django.conf import settings
import re
from apps.hospi.models import HospiTeam
from post_office import mail
EMAIL_REGEX = re.compile(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$")
class Command(BaseCommand):
    """
        Send email 
    """
    help = 'Send email with the given template'

    def handle(self, *args, **options):
        teams = HospiTeam.objects.filter(accomodation_status='confirmed')
        members = []
        for team in teams:
            members+=team.get_all_members()
        email_list=[]
        for user in members:
            email_id = user.user.email
            if EMAIL_REGEX.match(email_id):
                email_list.append(email_id)
        print "Sending emails to ", len(email_list), "users "
        unsubscribe_link = "dasdasdasei8rwer9f898fasd89a"
        mail.send(
            sender = settings.DEFAULT_MAIN_FROM_EMAIL,
            bcc = email_list,
            template = args[0],
            context = {'FEST_NAME': settings.FEST_NAME, 'SITE_URL': settings.SITE_URL, 'unsubscribe_link': unsubscribe_link},
            headers = {'List-Unsubscribe': unsubscribe_link}
        ) 
        self.stdout.write("All done")

