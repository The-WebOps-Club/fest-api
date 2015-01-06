# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'PushNotification.dialog_yes'
        db.alter_column(u'api_pushnotification', 'dialog_yes', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'PushNotification.dialog_no'
        db.alter_column(u'api_pushnotification', 'dialog_no', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

    def backwards(self, orm):

        # Changing field 'PushNotification.dialog_yes'
        db.alter_column(u'api_pushnotification', 'dialog_yes', self.gf('django.db.models.fields.TextField')(max_length=50, null=True))

        # Changing field 'PushNotification.dialog_no'
        db.alter_column(u'api_pushnotification', 'dialog_no', self.gf('django.db.models.fields.TextField')(max_length=50, null=True))

    models = {
        u'api.pushnotification': {
            'Meta': {'object_name': 'PushNotification'},
            'dialog_no': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'dialog_text': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'dialog_title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'dialog_yes': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'expiry': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 1, 13, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_version': ('django.db.models.fields.IntegerField', [], {'default': '2000'}),
            'message': ('django.db.models.fields.TextField', [], {'max_length': '2000'}),
            'min_version': ('django.db.models.fields.IntegerField', [], {'default': '200'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['api']