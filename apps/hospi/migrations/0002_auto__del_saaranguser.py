# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'SaarangUser'
        db.delete_table(u'hospi_saaranguser')


    def backwards(self, orm):
        # Adding model 'SaarangUser'
        db.create_table(u'hospi_saaranguser', (
            ('city', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('mobile', self.gf('django.db.models.fields.BigIntegerField')(max_length=10)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('saarang_id', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('fb_id', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('accomod_is_confirmed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('friend_list', self.gf('django.db.models.fields.TextField')(max_length=1000)),
            ('desk_id', self.gf('django.db.models.fields.CharField')(default='SA14D0000', max_length=20)),
            ('college', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('fb_token', self.gf('django.db.models.fields.TextField')(max_length=1000)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('activate_status', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=100)),
            ('college_id', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'hospi', ['SaarangUser'])


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
        u'hospi.allotment': {
            'Meta': {'object_name': 'Allotment'},
            'alloted_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'alloted_coord'", 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'alloted_team'", 'to': u"orm['hospi.HospiTeam']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'hospi.hospilog': {
            'Meta': {'object_name': 'HospiLog'},
            'checked_out': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'checked_out_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'hospi_check_out_erp_user'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'checkout_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'hospi_log_erp_user'", 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'hospi_room'", 'to': u"orm['hospi.Room']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'hospi_log_user'", 'to': u"orm['users.UserProfile']"})
        },
        u'hospi.hospiteam': {
            'Meta': {'object_name': 'HospiTeam'},
            'accomodation_status': ('django.db.models.fields.CharField', [], {'default': "'not_req'", 'max_length': '50'}),
            'checked_in': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'checked_out': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'date_of_arrival': ('django.db.models.fields.DateField', [], {'default': "'2014-01-08'", 'null': 'True', 'blank': 'True'}),
            'date_of_departure': ('django.db.models.fields.DateField', [], {'default': "'2014-01-11'", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'leader': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'hospi_team_leader'", 'to': u"orm['users.UserProfile']"}),
            'mattress_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'mattress_returned': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'hospi_team_members'", 'blank': 'True', 'to': u"orm['users.UserProfile']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'team_sid': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'time_of_arrival': ('django.db.models.fields.TimeField', [], {'default': "'23:00:00'", 'null': 'True', 'blank': 'True'}),
            'time_of_departure': ('django.db.models.fields.TimeField', [], {'default': "'10:00:00'", 'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'hospi.hostel': {
            'Meta': {'object_name': 'Hostel'},
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'hospi.room': {
            'Meta': {'object_name': 'Room'},
            'capacity': ('django.db.models.fields.IntegerField', [], {'max_length': '3'}),
            'hostel': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'parent_hostel'", 'to': u"orm['hospi.Hostel']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'occupants': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'room_occupant'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['users.UserProfile']"})
        },
        u'misc.college': {
            'Meta': {'object_name': 'College'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        u'users.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'accomod_is_confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'activate_status': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'activation_key': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            'branch': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'college': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['misc.College']", 'null': 'True', 'blank': 'True'}),
            'college_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'college_roll': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'desk_id': ('django.db.models.fields.CharField', [], {'default': "'SA14D0000'", 'max_length': '20'}),
            'dob': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '100'}),
            'fb_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'fb_token': ('django.db.models.fields.TextField', [], {'max_length': '1000'}),
            'friend_list': ('django.db.models.fields.TextField', [], {'max_length': '1000'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "'F'", 'max_length': '1'}),
            'gender_hospi': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'key_expires': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 10, 17, 0, 0)'}),
            'last_activity_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(1950, 1, 1, 0, 0)'}),
            'last_activity_ip': ('django.db.models.fields.IPAddressField', [], {'default': "'0.0.0.0'", 'max_length': '15'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'mobile': ('django.db.models.fields.BigIntegerField', [], {'max_length': '10'}),
            'mobile_number': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'saarang_id': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'school_student': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'send_mails': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'to': u"orm['auth.User']"}),
            'want_accomodation': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['hospi']