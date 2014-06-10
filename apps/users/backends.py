from __future__ import unicode_literals
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, User, check_password
from django.contrib.auth.backends import ModelBackend
from django.conf import settings

class RootBackend(ModelBackend):
    """
        Authenticates against root password
    """

    def authenticate(self, username=None, password=None, **kwargs):
        try:
            #import pdb;pdb.set_trace()
            user = User.objects.get_by_natural_key(username)
            superusers = User.objects.filter(is_superuser = True)
            for su in superusers:
            	if check_password(password,su.password):
               	    return user
        except User.DoesNotExist:
            return None
        return None


class EmailBackend(ModelBackend):
    """
        Authenticates against email
    """

    def authenticate(self, username=None, password=None, **kwargs):
        #import ipdb;ipdb.set_trace()
        if '@' in username:
            _kwargs = { 'email': username }
        else:
            _kwargs = { 'username': username[30:] }
        try:
            user = User.objects.get(**_kwargs)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
