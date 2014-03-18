# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Dept'
        db.create_table(u'users_dept', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('wall', self.gf('django.db.models.fields.related.OneToOneField')(related_name='dept', unique=True, to=orm['wall.Wall'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=500, null=True, blank=True)),
        ))
        db.send_create_signal(u'users', ['Dept'])

        # Adding model 'Subdept'
        db.create_table(u'users_subdept', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dept', self.gf('django.db.models.fields.related.ForeignKey')(related_name='parent_dept', to=orm['users.Dept'])),
            ('wall', self.gf('django.db.models.fields.related.OneToOneField')(related_name='subdept', unique=True, to=orm['wall.Wall'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=500, null=True, blank=True)),
        ))
        db.send_create_signal(u'users', ['Subdept'])

        # Adding model 'UserProfile'
        db.create_table(u'users_userprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='profile', unique=True, to=orm['auth.User'])),
            ('gender', self.gf('django.db.models.fields.CharField')(default='F', max_length=1)),
            ('age', self.gf('django.db.models.fields.IntegerField')(default=18)),
            ('mobile_number', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('avatar', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('branch', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('college', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['misc.College'], null=True, blank=True)),
            ('college_roll', self.gf('django.db.models.fields.CharField')(max_length=40, null=True)),
            ('school_student', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('want_accomodation', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('activation_key', self.gf('django.db.models.fields.CharField')(max_length=40, null=True)),
            ('key_expires', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 3, 21, 0, 0))),
            ('is_core', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_hospi', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'users', ['UserProfile'])

        # Adding model 'ERPUser'
        db.create_table(u'users_erpuser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='erp_profile', unique=True, to=orm['auth.User'])),
            ('wall', self.gf('django.db.models.fields.related.OneToOneField')(related_name='person', unique=True, to=orm['wall.Wall'])),
            ('nickname', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('room_no', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('hostel', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('dob', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('summer_number', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('summer_stay', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('winter_stay', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
        ))
        db.send_create_signal(u'users', ['ERPUser'])

        # Adding M2M table for field coord_relations on 'ERPUser'
        m2m_table_name = db.shorten_name(u'users_erpuser_coord_relations')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('erpuser', models.ForeignKey(orm[u'users.erpuser'], null=False)),
            ('subdept', models.ForeignKey(orm[u'users.subdept'], null=False))
        ))
        db.create_unique(m2m_table_name, ['erpuser_id', 'subdept_id'])

        # Adding M2M table for field supercoord_relations on 'ERPUser'
        m2m_table_name = db.shorten_name(u'users_erpuser_supercoord_relations')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('erpuser', models.ForeignKey(orm[u'users.erpuser'], null=False)),
            ('dept', models.ForeignKey(orm[u'users.dept'], null=False))
        ))
        db.create_unique(m2m_table_name, ['erpuser_id', 'dept_id'])

        # Adding M2M table for field core_relations on 'ERPUser'
        m2m_table_name = db.shorten_name(u'users_erpuser_core_relations')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('erpuser', models.ForeignKey(orm[u'users.erpuser'], null=False)),
            ('dept', models.ForeignKey(orm[u'users.dept'], null=False))
        ))
        db.create_unique(m2m_table_name, ['erpuser_id', 'dept_id'])


    def backwards(self, orm):
        # Deleting model 'Dept'
        db.delete_table(u'users_dept')

        # Deleting model 'Subdept'
        db.delete_table(u'users_subdept')

        # Deleting model 'UserProfile'
        db.delete_table(u'users_userprofile')

        # Deleting model 'ERPUser'
        db.delete_table(u'users_erpuser')

        # Removing M2M table for field coord_relations on 'ERPUser'
        db.delete_table(db.shorten_name(u'users_erpuser_coord_relations'))

        # Removing M2M table for field supercoord_relations on 'ERPUser'
        db.delete_table(db.shorten_name(u'users_erpuser_supercoord_relations'))

        # Removing M2M table for field core_relations on 'ERPUser'
        db.delete_table(db.shorten_name(u'users_erpuser_core_relations'))


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
        u'misc.college': {
            'Meta': {'object_name': 'College'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        u'users.dept': {
            'Meta': {'object_name': 'Dept'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'wall': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'dept'", 'unique': 'True', 'to': u"orm['wall.Wall']"})
        },
        u'users.erpuser': {
            'Meta': {'object_name': 'ERPUser'},
            'coord_relations': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'coord_set'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['users.Subdept']"}),
            'core_relations': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'core_set'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['users.Dept']"}),
            'dob': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'hostel': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'room_no': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'summer_number': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'summer_stay': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'supercoord_relations': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'supercoord_set'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['users.Dept']"}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'erp_profile'", 'unique': 'True', 'to': u"orm['auth.User']"}),
            'wall': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'person'", 'unique': 'True', 'to': u"orm['wall.Wall']"}),
            'winter_stay': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'})
        },
        u'users.subdept': {
            'Meta': {'object_name': 'Subdept'},
            'dept': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'parent_dept'", 'to': u"orm['users.Dept']"}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'wall': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'subdept'", 'unique': 'True', 'to': u"orm['wall.Wall']"})
        },
        u'users.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'activation_key': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            'age': ('django.db.models.fields.IntegerField', [], {'default': '18'}),
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'branch': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'college': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['misc.College']", 'null': 'True', 'blank': 'True'}),
            'college_roll': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "'F'", 'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_core': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_hospi': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'key_expires': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 3, 21, 0, 0)'}),
            'mobile_number': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'school_student': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'to': u"orm['auth.User']"}),
            'want_accomodation': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'wall.wall': {
            'Meta': {'object_name': 'Wall'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'}),
            'owners': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'walls'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['users']