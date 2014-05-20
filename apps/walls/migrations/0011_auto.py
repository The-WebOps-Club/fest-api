# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding M2M table for field access_users on 'Wall'
        m2m_table_name = db.shorten_name(u'walls_wall_access_users')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('wall', models.ForeignKey(orm[u'walls.wall'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['wall_id', 'user_id'])

        # Adding M2M table for field access_subdepts on 'Wall'
        m2m_table_name = db.shorten_name(u'walls_wall_access_subdepts')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('wall', models.ForeignKey(orm[u'walls.wall'], null=False)),
            ('subdept', models.ForeignKey(orm[u'users.subdept'], null=False))
        ))
        db.create_unique(m2m_table_name, ['wall_id', 'subdept_id'])

        # Adding M2M table for field access_depts on 'Wall'
        m2m_table_name = db.shorten_name(u'walls_wall_access_depts')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('wall', models.ForeignKey(orm[u'walls.wall'], null=False)),
            ('dept', models.ForeignKey(orm[u'users.dept'], null=False))
        ))
        db.create_unique(m2m_table_name, ['wall_id', 'dept_id'])

        # Adding M2M table for field access_pages on 'Wall'
        m2m_table_name = db.shorten_name(u'walls_wall_access_pages')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('wall', models.ForeignKey(orm[u'walls.wall'], null=False)),
            ('page', models.ForeignKey(orm[u'users.page'], null=False))
        ))
        db.create_unique(m2m_table_name, ['wall_id', 'page_id'])

        # Adding M2M table for field access_users on 'Post'
        m2m_table_name = db.shorten_name(u'walls_post_access_users')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('post', models.ForeignKey(orm[u'walls.post'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['post_id', 'user_id'])

        # Adding M2M table for field access_subdepts on 'Post'
        m2m_table_name = db.shorten_name(u'walls_post_access_subdepts')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('post', models.ForeignKey(orm[u'walls.post'], null=False)),
            ('subdept', models.ForeignKey(orm[u'users.subdept'], null=False))
        ))
        db.create_unique(m2m_table_name, ['post_id', 'subdept_id'])

        # Adding M2M table for field access_depts on 'Post'
        m2m_table_name = db.shorten_name(u'walls_post_access_depts')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('post', models.ForeignKey(orm[u'walls.post'], null=False)),
            ('dept', models.ForeignKey(orm[u'users.dept'], null=False))
        ))
        db.create_unique(m2m_table_name, ['post_id', 'dept_id'])

        # Adding M2M table for field access_pages on 'Post'
        m2m_table_name = db.shorten_name(u'walls_post_access_pages')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('post', models.ForeignKey(orm[u'walls.post'], null=False)),
            ('page', models.ForeignKey(orm[u'users.page'], null=False))
        ))
        db.create_unique(m2m_table_name, ['post_id', 'page_id'])


    def backwards(self, orm):
        # Removing M2M table for field access_users on 'Wall'
        db.delete_table(db.shorten_name(u'walls_wall_access_users'))

        # Removing M2M table for field access_subdepts on 'Wall'
        db.delete_table(db.shorten_name(u'walls_wall_access_subdepts'))

        # Removing M2M table for field access_depts on 'Wall'
        db.delete_table(db.shorten_name(u'walls_wall_access_depts'))

        # Removing M2M table for field access_pages on 'Wall'
        db.delete_table(db.shorten_name(u'walls_wall_access_pages'))

        # Removing M2M table for field access_users on 'Post'
        db.delete_table(db.shorten_name(u'walls_post_access_users'))

        # Removing M2M table for field access_subdepts on 'Post'
        db.delete_table(db.shorten_name(u'walls_post_access_subdepts'))

        # Removing M2M table for field access_depts on 'Post'
        db.delete_table(db.shorten_name(u'walls_post_access_depts'))

        # Removing M2M table for field access_pages on 'Post'
        db.delete_table(db.shorten_name(u'walls_post_access_pages'))


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
        u'users.dept': {
            'Meta': {'object_name': 'Dept'},
            'cache_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(1950, 1, 1, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'time_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(1950, 1, 1, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'wall': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'dept'", 'unique': 'True', 'to': u"orm['walls.Wall']"})
        },
        u'users.page': {
            'Meta': {'object_name': 'Page'},
            'cache_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(1950, 1, 1, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'time_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(1950, 1, 1, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'wall': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'page'", 'unique': 'True', 'to': u"orm['walls.Wall']"})
        },
        u'users.subdept': {
            'Meta': {'object_name': 'Subdept'},
            'cache_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(1950, 1, 1, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'dept': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subdepts'", 'to': u"orm['users.Dept']"}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'time_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(1950, 1, 1, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'wall': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'subdept'", 'unique': 'True', 'to': u"orm['walls.Wall']"})
        },
        u'walls.comment': {
            'Meta': {'object_name': 'Comment'},
            'by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comment_created'", 'to': u"orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'liked_users': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'liked_comment'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'time_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'walls.post': {
            'Meta': {'object_name': 'Post'},
            'access_depts': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'access_post'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['users.Dept']"}),
            'access_pages': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'access_post'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['users.Page']"}),
            'access_subdepts': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'access_post'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['users.Subdept']"}),
            'access_users': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'access_post'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'post_created'", 'to': u"orm['auth.User']"}),
            'comments': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'parent_post'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['walls.Comment']"}),
            'comments_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'liked_users': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'liked_post'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'notification_depts': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'notified_post'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['users.Dept']"}),
            'notification_pages': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'notified_post'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['users.Page']"}),
            'notification_subdepts': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'notified_post'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['users.Subdept']"}),
            'notification_users': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'notified_post'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'time_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'wall': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'posts'", 'null': 'True', 'to': u"orm['walls.Wall']"})
        },
        u'walls.wall': {
            'Meta': {'object_name': 'Wall'},
            'access_depts': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'access_wall'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['users.Dept']"}),
            'access_pages': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'access_wall'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['users.Page']"}),
            'access_subdepts': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'access_wall'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['users.Subdept']"}),
            'access_users': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'access_wall'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'cache_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(1950, 1, 1, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'notification_depts': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'notified_wall'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['users.Dept']"}),
            'notification_pages': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'notified_wall'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['users.Page']"}),
            'notification_subdepts': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'notified_wall'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['users.Subdept']"}),
            'notification_users': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'notified_wall'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'time_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(1950, 1, 1, 0, 0)', 'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['walls']