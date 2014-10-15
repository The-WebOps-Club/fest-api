# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Hostel'
        db.create_table(u'hospi_hostel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal(u'hospi', ['Hostel'])

        # Adding model 'Room'
        db.create_table(u'hospi_room', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('hostel', self.gf('django.db.models.fields.related.ForeignKey')(related_name='parent_hostel', to=orm['hospi.Hostel'])),
            ('capacity', self.gf('django.db.models.fields.IntegerField')(max_length=3)),
        ))
        db.send_create_signal(u'hospi', ['Room'])

        # Adding M2M table for field occupants on 'Room'
        m2m_table_name = db.shorten_name(u'hospi_room_occupants')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('room', models.ForeignKey(orm[u'hospi.room'], null=False)),
            ('userprofile', models.ForeignKey(orm[u'users.userprofile'], null=False))
        ))
        db.create_unique(m2m_table_name, ['room_id', 'userprofile_id'])

        # Adding model 'HospiTeam'
        db.create_table(u'hospi_hospiteam', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('leader', self.gf('django.db.models.fields.related.ForeignKey')(related_name='hospi_team_leader', to=orm['users.UserProfile'])),
            ('team_sid', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('accomodation_status', self.gf('django.db.models.fields.CharField')(default='not_req', max_length=50)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('date_of_arrival', self.gf('django.db.models.fields.DateField')(default='2014-01-08', null=True, blank=True)),
            ('time_of_arrival', self.gf('django.db.models.fields.TimeField')(default='23:00:00', null=True, blank=True)),
            ('date_of_departure', self.gf('django.db.models.fields.DateField')(default='2014-01-11', null=True, blank=True)),
            ('time_of_departure', self.gf('django.db.models.fields.TimeField')(default='10:00:00', null=True, blank=True)),
            ('checked_in', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('checked_out', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('mattress_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('mattress_returned', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'hospi', ['HospiTeam'])

        # Adding M2M table for field members on 'HospiTeam'
        m2m_table_name = db.shorten_name(u'hospi_hospiteam_members')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('hospiteam', models.ForeignKey(orm[u'hospi.hospiteam'], null=False)),
            ('userprofile', models.ForeignKey(orm[u'users.userprofile'], null=False))
        ))
        db.create_unique(m2m_table_name, ['hospiteam_id', 'userprofile_id'])

        # Adding model 'Allotment'
        db.create_table(u'hospi_allotment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(related_name='alloted_team', to=orm['hospi.HospiTeam'])),
            ('alloted_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='alloted_coord', to=orm['auth.User'])),
        ))
        db.send_create_signal(u'hospi', ['Allotment'])

        # Adding model 'HospiLog'
        db.create_table(u'hospi_hospilog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='hospi_log_erp_user', to=orm['auth.User'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='hospi_log_user', to=orm['users.UserProfile'])),
            ('room', self.gf('django.db.models.fields.related.ForeignKey')(related_name='hospi_room', to=orm['hospi.Room'])),
            ('checked_out', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('checkout_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('checked_out_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='hospi_check_out_erp_user', null=True, to=orm['auth.User'])),
        ))
        db.send_create_signal(u'hospi', ['HospiLog'])

        # Adding model 'SaarangUser'
        db.create_table(u'hospi_saaranguser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('saarang_id', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('desk_id', self.gf('django.db.models.fields.CharField')(default='SA14D0000', max_length=20)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=100)),
            ('mobile', self.gf('django.db.models.fields.BigIntegerField')(max_length=10)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('fb_id', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('friend_list', self.gf('django.db.models.fields.TextField')(max_length=1000)),
            ('college', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('college_id', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('fb_token', self.gf('django.db.models.fields.TextField')(max_length=1000)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('activate_status', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('accomod_is_confirmed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'hospi', ['SaarangUser'])


    def backwards(self, orm):
        # Deleting model 'Hostel'
        db.delete_table(u'hospi_hostel')

        # Deleting model 'Room'
        db.delete_table(u'hospi_room')

        # Removing M2M table for field occupants on 'Room'
        db.delete_table(db.shorten_name(u'hospi_room_occupants'))

        # Deleting model 'HospiTeam'
        db.delete_table(u'hospi_hospiteam')

        # Removing M2M table for field members on 'HospiTeam'
        db.delete_table(db.shorten_name(u'hospi_hospiteam_members'))

        # Deleting model 'Allotment'
        db.delete_table(u'hospi_allotment')

        # Deleting model 'HospiLog'
        db.delete_table(u'hospi_hospilog')

        # Deleting model 'SaarangUser'
        db.delete_table(u'hospi_saaranguser')


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
        u'hospi.saaranguser': {
            'Meta': {'object_name': 'SaarangUser'},
            'accomod_is_confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'activate_status': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'college': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'college_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'desk_id': ('django.db.models.fields.CharField', [], {'default': "'SA14D0000'", 'max_length': '20'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '100'}),
            'fb_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'fb_token': ('django.db.models.fields.TextField', [], {'max_length': '1000'}),
            'friend_list': ('django.db.models.fields.TextField', [], {'max_length': '1000'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'mobile': ('django.db.models.fields.BigIntegerField', [], {'max_length': '10'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'saarang_id': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
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