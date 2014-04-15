# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'StoredCredential'
        db.create_table(u'docs_storedcredential', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('user_id', self.gf('django.db.models.fields.TextField')()),
            ('credentials', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'docs', ['StoredCredential'])


    def backwards(self, orm):
        # Deleting model 'StoredCredential'
        db.delete_table(u'docs_storedcredential')


    models = {
        u'docs.storedcredential': {
            'Meta': {'object_name': 'StoredCredential'},
            'credentials': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user_id': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['docs']