# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Category.updated'
        db.add_column(u'core_category', 'updated',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


        # Changing field 'Source.title'
        db.alter_column(u'core_source', 'title', self.gf('django.db.models.fields.CharField')(max_length=255))
        # Adding field 'Param.updated'
        db.add_column(u'core_param', 'updated',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Product.updated'
        db.add_column(u'core_product', 'updated',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Category.updated'
        db.delete_column(u'core_category', 'updated')


        # Changing field 'Source.title'
        db.alter_column(u'core_source', 'title', self.gf('django.db.models.fields.TextField')())
        # Deleting field 'Param.updated'
        db.delete_column(u'core_param', 'updated')

        # Deleting field 'Product.updated'
        db.delete_column(u'core_product', 'updated')


    models = {
        u'core.category': {
            'Meta': {'object_name': 'Category'},
            'external_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['core.Category']"}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'categories'", 'to': u"orm['core.Source']"}),
            'updated': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'core.param': {
            'Meta': {'object_name': 'Param'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'params'", 'to': u"orm['core.Product']"}),
            'updated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'core.product': {
            'Meta': {'object_name': 'Product'},
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'products'", 'symmetrical': 'False', 'to': u"orm['core.Category']"}),
            'external_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'products'", 'to': u"orm['core.Source']"}),
            'updated': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
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