# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'NewsItem'
        db.create_table(u'newsletter_newsitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=96, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')(max_length=256, blank=True)),
            ('date_to_publish', self.gf('django.db.models.fields.DateField')(null=True)),
            ('create_date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('position', self.gf('django.db.models.fields.IntegerField')(blank=True)),
        ))
        db.send_create_signal(u'newsletter', ['NewsItem'])

        # Adding model 'NewsImage'
        db.create_table(u'newsletter_newsimage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('news_item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['newsletter.NewsItem'])),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'newsletter', ['NewsImage'])


    def backwards(self, orm):
        # Deleting model 'NewsItem'
        db.delete_table(u'newsletter_newsitem')

        # Deleting model 'NewsImage'
        db.delete_table(u'newsletter_newsimage')


    models = {
        u'newsletter.newsimage': {
            'Meta': {'object_name': 'NewsImage'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'news_item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['newsletter.NewsItem']"})
        },
        u'newsletter.newsitem': {
            'Meta': {'object_name': 'NewsItem'},
            'content': ('django.db.models.fields.TextField', [], {'max_length': '256', 'blank': 'True'}),
            'create_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_to_publish': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '96', 'blank': 'True'})
        }
    }

    complete_apps = ['newsletter']