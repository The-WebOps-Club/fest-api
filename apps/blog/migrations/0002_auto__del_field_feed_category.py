# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Feed.category'
        db.delete_column(u'blog_feed', 'category_id')

        # Adding M2M table for field feeds on 'Category'
        m2m_table_name = db.shorten_name(u'blog_category_feeds')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('category', models.ForeignKey(orm[u'blog.category'], null=False)),
            ('feed', models.ForeignKey(orm[u'blog.feed'], null=False))
        ))
        db.create_unique(m2m_table_name, ['category_id', 'feed_id'])


    def backwards(self, orm):
        # Adding field 'Feed.category'
        db.add_column(u'blog_feed', 'category',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='feeds', to=orm['blog.Category']),
                      keep_default=False)

        # Removing M2M table for field feeds on 'Category'
        db.delete_table(db.shorten_name(u'blog_category_feeds'))


    models = {
        u'blog.category': {
            'Meta': {'object_name': 'Category'},
            'feeds': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'feeds'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['blog.Feed']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'blog.feed': {
            'Meta': {'object_name': 'Feed'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['blog']