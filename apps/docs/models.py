import pickle
import base64

from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models

from oauth2client.django_orm import FlowField
from oauth2client.django_orm import CredentialsField

# These two lines make South aware of the new Field type
# from south.modelsinspector import add_introspection_rules
# add_introspection_rules([], ["^apps\.docs\.oauth2client\.django_orm\.CredentialsField"])


class CredentialsModel(models.Model):
    id = models.ForeignKey(User, primary_key=True)
    credential = models.TextField(blank=True, null=True)
    refresh_token = models.TextField(blank=True, null=True)

class CredentialsAdmin(admin.ModelAdmin):
    pass


admin.site.register(CredentialsModel, CredentialsAdmin)

# class  FileInfo