# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DataBlob'
        db.create_table(u'webmirror_datablob', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('data', self.gf('django.db.models.fields.TextField')(max_length=5000)),
        ))
        db.send_create_signal(u'webmirror', ['DataBlob'])


    def backwards(self, orm):
        # Deleting model 'DataBlob'
        db.delete_table(u'webmirror_datablob')


    models = {
        u'webmirror.datablob': {
            'Meta': {'object_name': 'DataBlob'},
            'data': ('django.db.models.fields.TextField', [], {'max_length': '5000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['webmirror']