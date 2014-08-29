# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'DataBlob.cluster'
        db.add_column(u'webmirror_datablob', 'cluster',
                      self.gf('django.db.models.fields.CharField')(default='EVNT', max_length=5),
                      keep_default=False)


        # Changing field 'DataBlob.ref'
        db.alter_column(u'webmirror_datablob', 'ref', self.gf('django.db.models.fields.CharField')(max_length=10))

    def backwards(self, orm):
        # Deleting field 'DataBlob.cluster'
        db.delete_column(u'webmirror_datablob', 'cluster')


        # Changing field 'DataBlob.ref'
        db.alter_column(u'webmirror_datablob', 'ref', self.gf('django.db.models.fields.CharField')(max_length=3))

    models = {
        u'webmirror.datablob': {
            'Meta': {'object_name': 'DataBlob'},
            'cluster': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'data': ('django.db.models.fields.TextField', [], {'max_length': '5000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ref': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['webmirror']