# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Product.source'
        db.delete_column(u'core_product', 'source_id')


    def backwards(self, orm):
        # Adding field 'Product.source'
        db.add_column(u'core_product', 'source',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, related_name='products', to=orm['core.Source']),
                      keep_default=False)


    models = {
        u'core.category': {
            'Meta': {'object_name': 'Category'},
            'external_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['core.Category']"}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'categories'", 'to': u"orm['core.Source']"}),
            'updated': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'core.param': {
            'Meta': {'object_name': 'Param'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'params'", 'to': u"orm['core.Product']"}),
            'updated': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'core.product': {
            'Meta': {'object_name': 'Product'},
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'products'", 'symmetrical': 'False', 'to': u"orm['core.Category']"}),
            'external_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'core.source': {
            'Meta': {'object_name': 'Source'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parser': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'sync_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['core']