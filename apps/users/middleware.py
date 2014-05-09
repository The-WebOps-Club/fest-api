from social.apps.django_app.middleware import SocialAuthExceptionMiddleware
from social.exceptions import SocialAuthBaseException, \
    NotAllowedToDisconnect, AuthException, AuthFailed, \
    AuthCanceled, AuthUnknownError, AuthAlreadyAssociated, \
    AuthForbidden

from apps.users.models import UserProfile
from django.conf import settings
from django.core.cache import cache
from django.contrib.sites.models import Site
from datetime import datetime
import re


class CustomSocialAuthExceptionMiddleware(SocialAuthExceptionMiddleware):
    def process_exception(self, request, exception):
        self.strategy = getattr(request, 'social_strategy', None)
        if self.strategy is None or self.raise_exception(request, exception):
            return
        print "---------------------------------------"
        print exception
        return redirect('misc.views.err404', kwargs={'messages':['Ouchie. Social', message]})
        if isinstance(exception, AuthAlreadyAssociated):
            return redirect('misc.views.err404', kwargs={'messages':['Ouchie. Social', message]})
        if 1 or isinstance(exception, SocialAuthBaseException):
            message = self.get_message(request, exception)
            return redirect('misc.views.err404', kwargs={'messages':['Ouchie. Social', message]})

        raise exception

    def raise_exception(self, request, exception):
        return self.strategy.setting('RAISE_EXCEPTIONS', settings.DEBUG)

    def get_message(self, request, exception):
        return six.text_type(exception)

    def get_redirect_uri(self, request, exception):
        return self.strategy.setting('LOGIN_ERROR_URL')


compiledLists = {}
 
class LastActivityDatabaseMiddleware(object):
    def process_request(self, request):
        if not request.user.is_authenticated():
            return
        try:
            activity = request.user.profile
        except:
            return
        urlsModule = __import__(settings.ROOT_URLCONF, {}, {}, [''])
        skipList = getattr(urlsModule, 'skip_last_activity_date', None)
        skippedPath = request.path
        if skippedPath.startswith('/'):
            skippedPath = skippedPath[1:]
        if skipList is not None:
            for expression in skipList:
                compiledVersion = None
                if not compiledLists.has_key(expression):
                    compiledLists[expression] = re.compile(expression)
                compiledVersion = compiledLists[expression]
                if compiledVersion.search(skippedPath):
                    return
        activity.last_activity_date = datetime.now()
        activity.last_activity_ip = request.META['REMOTE_ADDR']
        activity.save()


class LastActivityCacheMiddleware:
    def process_request(self, request):
        current_user = request.user
        if request.user.is_authenticated():
            now = datetime.now()
            cache.set('seen_%s' % (current_user.username), now, 
                           settings.USER_LASTSEEN_TIMEOUT)