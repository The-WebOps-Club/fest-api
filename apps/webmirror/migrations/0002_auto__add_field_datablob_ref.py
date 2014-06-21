# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'DataBlob.ref'
        db.add_column(u'webmirror_datablob', 'ref',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=3),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'DataBlob.ref'
        db.delete_column(u'webmirror_datablob', 'ref')


    models = {
        u'webmirror.datablob': {
            'Meta': {'object_name': 'DataBlob'},
            'data': ('django.db.models.fields.TextField', [], {'max_length': '5000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ref': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        }
    }

    complete_apps = ['webmirror']