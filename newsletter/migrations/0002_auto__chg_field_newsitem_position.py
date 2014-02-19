# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'NewsItem.position'
        db.alter_column(u'newsletter_newsitem', 'position', self.gf('django.db.models.fields.IntegerField')(null=True))

    def backwards(self, orm):

        # Changing field 'NewsItem.position'
        db.alter_column(u'newsletter_newsitem', 'position', self.gf('django.db.models.fields.IntegerField')(default=0))

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
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '96', 'blank': 'True'})
        }
    }

    complete_apps = ['newsletter']