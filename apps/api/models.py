
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import models
import datetime
from django.conf import settings
import requests
import json
class PushNotification(models.Model):
    expiry = models.DateTimeField(default=datetime.datetime(2015,01,13,23,59), help_text="Expiry date for the message")
    title = models.CharField(max_length=100, help_text="Title for the message")
    message = models.TextField(max_length=2000, help_text="Message text to be displayed")
    url = models.CharField(max_length=500,help_text="URL to redirect when clicked on notification", default="content://com.saarang.samples.apps.iosched/sessions")
    dialog_title = models.CharField(max_length=200, blank=True, null=True, help_text="Not required, fill only if a dialog needs to be shown")
    dialog_text = models.TextField(max_length=1000, blank=True, null=True,help_text="Not required, fill only if a dialog needs to be shown")
    dialog_yes = models.CharField(max_length=50, blank=True, null=True,help_text="Not required, fill only if a dialog needs to be shown, text on YES button, redirect to URL")
    dialog_no = models.CharField(max_length=50, blank=True, null=True,help_text="Not required, fill only if a dialog needs to be shown, text on NO button, dissmiss dialog")
    min_version = models.IntegerField(default=200,help_text="Dont change unless you know what this is.")
    max_version = models.IntegerField(default=2000,help_text="Dont change unless you know what this is.")
    status = models.TextField(max_length=2000, blank=True, null=True)
    
    def __unicode__(self):
        return self.title

def check_if_dialog_exist(notif):
    if notif.dialog_title and notif.dialog_text and notif.dialog_yes and notif.dialog_no:
        return True
    else:
        return False

@receiver(post_save, sender=PushNotification)
def send_notification(sender, **kwargs):
    notif = kwargs['instance']
    created = kwargs['created']
    print "PushNotif"
    print created
    params = {
        "format": "1.0.00",
        'audience' : 'all',
        'expiry': str((notif.expiry+datetime.timedelta(hours=5,minutes=30)).strftime('%Y-%m-%dT%H:%M:%SZ')),
        'title':str(notif.title),
        'message': str(notif.message),
        'url':str(notif.url),
        'minVersion': str(notif.min_version),
        'maxVersion': str(notif.max_version)
    }
    if check_if_dialog_exist(notif):
        params['dialogTitle'] = str(notif.dialog_title)
        params['dialogText'] = str(notif.dialog_text)
        params['dialogYes'] = str(notif.dialog_yes)
        params['dialogNo'] = str(notif.dialog_no)
    headers = {
        'Authorization': 'key='+settings.APP_ENGINE_ADMIN_KEY,
        'Content-Type': 'application/octet-stream'
    }
    url = 'https://light-lambda-567.appspot.com/send/global/notification/'
    print params
    print headers

    if created:
        r = requests.post(url, data=json.dumps(params), headers=headers) 
        resp = str(r.status_code) 
        print r.status_code
        notif.satus = resp
        notif.save()
