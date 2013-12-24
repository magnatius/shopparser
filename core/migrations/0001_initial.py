# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Source'
        db.create_table(u'core_source', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.TextField')()),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('sync_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('parser', self.gf('django.db.models.fields.CharField')(max_length=250)),
        ))
        db.send_create_signal(u'core', ['Source'])


    def backwards(self, orm):
        # Deleting model 'Source'
        db.delete_table(u'core_source')


    models = {
        u'core.source': {
            'Meta': {'object_name': 'Source'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parser': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'sync_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['core']