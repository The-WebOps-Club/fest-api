# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding M2M table for field category on 'Feed'
        m2m_table_name = db.shorten_name(u'blog_feed_category')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('feed', models.ForeignKey(orm[u'blog.feed'], null=False)),
            ('category', models.ForeignKey(orm[u'blog.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['feed_id', 'category_id'])

        # Removing M2M table for field feeds on 'Category'
        db.delete_table(db.shorten_name(u'blog_category_feeds'))


    def backwards(self, orm):
        # Removing M2M table for field category on 'Feed'
        db.delete_table(db.shorten_name(u'blog_feed_category'))

        # Adding M2M table for field feeds on 'Category'
        m2m_table_name = db.shorten_name(u'blog_category_feeds')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('category', models.ForeignKey(orm[u'blog.category'], null=False)),
            ('feed', models.ForeignKey(orm[u'blog.feed'], null=False))
        ))
        db.create_unique(m2m_table_name, ['category_id', 'feed_id'])


    models = {
        u'blog.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'blog.feed': {
            'Meta': {'object_name': 'Feed'},
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'feeds'", 'symmetrical': 'False', 'to': u"orm['blog.Category']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['blog']