from apps.users.token import default_token_generator as pset
from django.utils.http import int_to_base36, base36_to_int
from post_office import mail

def send_email_validation_mail(user):
    code = int_to_base36(user.id) + '-' + pset.make_token(user) 
    unsubscribe_link = recipient.profile.create_unsubscribe_link()
    mail.send({
        'sender': settings.DEFAULT_FROM_EMAIL,
        'recipients': [user.email],
        'template': 'validation.email',
        'context': {'subject': 'Validate your email, Saarang 2015', 'user': user, 'FEST_NAME': settings.FEST_NAME, 'SITE_URL': settings.SITE_URL, 'unsubscribe_link': unsubscribe_link, 'code':code},
        'headers': {'List-Unsubscribe': unsubscribe_link},
    }) 
    return 

def send_registration_mail(user):
    mail.send({
        'sender': settings.DEFAULT_FROM_EMAIL,
        'recipients': [user.email],
        'template': 'registration.email',
        'context': {'subject': 'Welcome to Saarang 2015', 'user': user, 'FEST_NAME': settings.FEST_NAME, 'SITE_URL': settings.SITE_URL},
        'headers': {'List-Unsubscribe': unsubscribe_link},
    }) 
    return 

