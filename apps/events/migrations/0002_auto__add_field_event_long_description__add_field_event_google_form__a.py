# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Event.long_description'
        db.add_column(u'events_event', 'long_description',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Event.google_form'
        db.add_column(u'events_event', 'google_form',
                      self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Event.event_image'
        db.add_column(u'events_event', 'event_image',
                      self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Event.long_description'
        db.delete_column(u'events_event', 'long_description')

        # Deleting field 'Event.google_form'
        db.delete_column(u'events_event', 'google_form')

        # Deleting field 'Event.event_image'
        db.delete_column(u'events_event', 'event_image')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'events.event': {
            'Meta': {'object_name': 'Event'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'coords': ('select2.fields.ManyToManyField', [], {'related_name': "'coord_events'", 'to': u"orm['users.ERPProfile']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True', 'search_field': 'None'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'event_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'event_type': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'google_form': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'google_group': ('django.db.models.fields.EmailField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'has_tdp': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'long_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'registration_ends': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'registration_starts': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'short_description': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'team_size_max': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'}),
            'team_size_min': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'}),
            'teams_registered': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'events_registered'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['users.Team']"}),
            'users_registered': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'events_registered'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"})
        },
        u'events.eventtab': {
            'Meta': {'object_name': 'EventTab'},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['events.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'events.tab': {
            'Meta': {'ordering': "['order']", 'object_name': 'Tab'},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'event': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['events.Event']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'head': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'users.dept': {
            'Meta': {'object_name': 'Dept'},
            'cache_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(1950, 1, 1, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'calendar_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'directory_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'time_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(1950, 1, 1, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'wall': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'dept'", 'unique': 'True', 'to': u"orm['walls.Wall']"})
        },
        u'users.erpprofile': {
            'Meta': {'object_name': 'ERPProfile'},
            'coord_relations': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'coord_set'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['users.Subdept']"}),
            'core_relations': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'core_set'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['users.Dept']"}),
            'hostel': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'page_relations': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'user_set'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['users.Page']"}),
            'room_no': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'summer_number': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'summer_stay': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'summer_stay2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'supercoord_relations': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'supercoord_set'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['users.Dept']"}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'erp_profile'", 'unique': 'True', 'to': u"orm['auth.User']"}),
            'wall': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'person'", 'unique': 'True', 'to': u"orm['walls.Wall']"}),
            'winter_stay': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'winter_stay2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'users.page': {
            'Meta': {'object_name': 'Page'},
            'cache_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(1950, 1, 1, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'calendar_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'directory_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'time_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(1950, 1, 1, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'wall': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'page'", 'unique': 'True', 'to': u"orm['walls.Wall']"})
        },
        u'users.subdept': {
            'Meta': {'object_name': 'Subdept'},
            'cache_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(1950, 1, 1, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'dept': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subdepts'", 'to': u"orm['users.Dept']"}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'directory_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'time_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(1950, 1, 1, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'wall': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'subdept'", 'unique': 'True', 'to': u"orm['walls.Wall']"})
        },
        u'users.team': {
            'Meta': {'object_name': 'Team'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'teams'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'walls.wall': {
            'Meta': {'object_name': 'Wall'},
            'access_depts': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'access_wall'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['users.Dept']"}),
            'access_pages': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'access_wall'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['users.Page']"}),
            'access_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'access_subdepts': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'access_wall'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['users.Subdept']"}),
            'access_users': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'access_wall'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'cache_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(1950, 1, 1, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'notification_depts': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'notified_wall'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['users.Dept']"}),
            'notification_pages': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'notified_wall'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['users.Page']"}),
            'notification_subdepts': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'notified_wall'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['users.Subdept']"}),
            'notification_users': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'notified_wall'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'time_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(1950, 1, 1, 0, 0)', 'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['events']