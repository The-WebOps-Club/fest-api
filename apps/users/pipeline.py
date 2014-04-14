# Django
from django.conf import settings
from django.core.signing import Signer
from django.template.loader import get_template
from django.template.context import Context, RequestContext
from django.utils.html import strip_tags
from django.shortcuts import render_to_response, redirect, HttpResponseRedirect
from django.core.urlresolvers import resolve, reverse
from django.core.mail import EmailMultiAlternatives
# Apps
# Decorators
# Models
from django.contrib.auth.models import User
from apps.walls.models import Wall
from apps.events.models import Event
from apps.users.models import ERPProfile, Dept, Subdept
from django.contrib import messages
# Forms
# View functions
# Misc
from misc.utils import *
import facebook
from social.pipeline.partial import partial
from post_office import mail
# Python
import datetime
from urlparse import parse_qs
from smtplib import SMTPRecipientsRefused

# @partial
# def require_email(strategy, details, user=None, is_new=False, *args, **kwargs):
#     if user and user.email:
#         return
#     elif is_new and not details.get('email'):
#         if strategy.session_get('saved_email'):
#             print 'Adding email to details.'
#             details['email'] = strategy.session_pop('saved_email')
#             print details
#         else:
#             # request = kwargs['request']
#             # request.session['signup_in_progress'] = True
#             # return HttpResponseRedirect(reverse('accounts.views.mobile_signup_details', email_backend = True))
#             return redirect('accounts.views.mobile_signup_details')

# @partial
# def user_details_for_email_signup(strategy, details, user = None, is_new = False, *args, **kwargs):
#     # print 'user_details_for_email_signup'
#     # print strategy.backend.name
#     # print 'user is there: ', str(user != None)
#     # print 'user:', user
#     # print 'details ', details
#     if strategy.backend.name is not 'email':
#         return
#     if user and user.email and user.first_name and user.last_name and user.has_usable_password():
#         return
#     elif is_new and not (details.get('email') and details.get('first_name') and details.get('last_name') and details.get('password')):
#         if strategy.session_get('saved_email'):
#             details['email'] = strategy.session_pop('saved_email')
#         if strategy.session_get('saved_first_name'):
#             details['first_name'] = strategy.session_pop('saved_first_name')
#         if strategy.session_get('saved_last_name'):
#             details['last_name'] = strategy.session_pop('saved_last_name')
#         if strategy.session_get('saved_password'):
#             details['password'] = strategy.session_pop('saved_password')
#         if not (details.get('email') and details.get('first_name') and details.get('last_name') and details.get('password')):
#             return redirect('accounts.views.mobile_signup_details')

# @partial
# def save_password(strategy, details, user = None, is_new = False, new_association = False, *args, **kwargs):
#     if strategy.backend.name != 'email':
#         return

#     if not is_new:
#         return
#     password = details['password']
#     if is_new:
#         user.set_password(password)
#         user.save()
#     elif not user.check_password(password):
#         # return {'user': None, 'social': None}
#         raise AuthException(strategy.backend)

# #Create user profile
# @partial
# def create_user_profile(strategy, details, user = None, is_new = False, *args, **kwargs):
#     # deactivate_external_user(user)
#     try:
#         (userprofile, created_now) = user.userprofile_set.get_or_create()
#     except Exception, e:
#         pass

# #Send welcome mail
# @partial
# def send_welcome_mail(strategy, details, user = None, is_new = False, *args, **kwargs):
#     # print is_new
#     # print new_association
#     if strategy.backend.name == 'email' and user is not None:
#         user.is_active = True
#         user.save()
#         is_new = True
#     if not (is_new and user != None):
#         return
#     try:
#         userprofile = user.get_profile()
#     except:
#         userprofile = None
#     #A little weird. If I have already logged in with google with some email, and I use the same email for Facebook and I login with that, is_new is still set to True because it is a new login. new_association is redundant - it is always true.
#     # Update: This seems to be fixed in the new version (0.1.22). Must check.
#     if is_new and userprofile == None:
#         #Must send email
#         signer = Signer(salt=user.email)
#         signedvalue = signer.sign(user.email)
#         if settings.SEND_EMAILS == True:
#             try :
#                 mail.send(
#                     [user.email], settings.DEFAULT_FROM_EMAIL,
#                     template='welcome.email',
#                     context={'user':user,'SITE_URL': settings.SITE_URL, 'unsubscribe':signedvalue},
#                     headers = {'List-Unsubscribe': reverse('accounts.views.unsubscribe',kwargs=dict(user_email=signedvalue))},
#                 )
#             except SMTPRecipientsRefused:
#                 messages.error(strategy.request,'<strong>Uh oh.</strong> The email ID you\'ve entered doesn\'t seem to be valid. We are unable to welcome you via email.',extra_tags='alert-error', fail_silently = True)
#         messages.success(strategy.request,'<strong>Welcome to the change!</strong> Please take a minute to update your details.',extra_tags='alert-success', fail_silently = True)


# #Social Stories
# @partial
# def social_story_on_join(strategy, details, social = None, user=None, is_new=False, new_association = False, *args, **kwargs):
#     backend = strategy.backend
#     if backend.name == 'twitter':
#         if is_new or new_association:
#             oauth_token = social.extra_data['access_token']['oauth_token']
#             oauth_secret = social.extra_data['access_token']['oauth_token_secret']
#             # parsed_tokens = parse_qs(access_token)
#             # oauth_token = parse_qs(access_token)
#             # oauth_secret = parse_qs(access_secret)
#             t = twitter.Twitter(
#                 auth=twitter.OAuth(
#                         oauth_token, oauth_secret,
#                         SOCIAL_AUTH_TWITTER_KEY, SOCIAL_AUTH_TWITTER_SECRET
#                     )
#                 )
#             try:
#                 t.statuses.update(status='Joined a network of Blood donors @bloodlinelabs #bloodline http://bloodlinelabs.com/')
#                 # print 'tweeting'
#             except:
#                 print "Some twitter error"
    
#     if backend.name == 'facebook':
#         if is_new or new_association:
#             access_token = social.extra_data['access_token']
#             #parsed_tokens = parse_qs(access_token)
#             #oauth_token = parsed_tokens['oauth_token'][0]
#             try:
#                 graph = facebook.GraphAPI(access_token)
#                 print graph.put_object("me", "bloodline_labs:join", blood=SITE_URL)
#                 # print 'facebooking'
#             except:
#                 print "Some Facebook error, mostly user didn't set publish permission"

#     return None

# # This function sends the validation email. Note: This is not a partial pipeline. It is in the pipeline file solely because it falls under the PSA category.
# def send_email_validation(strategy, code):
#     # print code.code
#     url = strategy.build_absolute_uri(reverse('social:complete', args = (strategy.backend.name, ))) + '?verification_code=' + code.code
#     # print url
#     try :
#         mail.send(
#             [code.email], settings.DEFAULT_FROM_EMAIL, template='email_validation.email',
#             context={'code':code,'url':url, 'SITE_URL': settings.SITE_URL}
#         )
#     except SMTPRecipientsRefused:
#         messages.error(strategy.request,'<strong>Uh oh.</strong> The email ID you\'ve entered doesn\'t seem to be valid. We are unable to send you the verification code.',extra_tags='alert-error', fail_silently = True)
#         return redirect('bloodline_server.views.home')

# # To simply display a template that says the validation email was sent.
# # TODO: Include a form here that takes in the code and redirects to the correct URL.
# def validation_sent(request):
#     messages.success(request,'<strong>Almost there ...</strong> We\'ve sent you an email at ' + request.session.get('email_validation_address','your email address') + '. Just click on the link.',extra_tags='alert-success', fail_silently = True)
#     return redirect('bloodline_server.views.home')

# @partial
# def miscellaneous(strategy, details, user = None, is_new = False, *args, **kwargs):
#     if is_new:
#         try:
#             new_user = CampaignUser.objects.get(email=user.email)
#             new_user.blacklisted = True
#             new_user.joined = True
#             new_user.save()
#         except CampaignUser.DoesNotExist:
#             pass
#     else:
#         pass
