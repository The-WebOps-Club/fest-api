import pickle
import base64

from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models

from oauth2client.django_orm import FlowField
from oauth2client.django_orm import CredentialsField

class FileInfo(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    file_id = models.CharField(max_length=200)
    metadata = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return str(self.timestamp) + str(self.name)

