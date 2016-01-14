# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'C2OProduct'
        db.create_table('catalogue_c2oproduct', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('unique_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('file_url', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('print_position', self.gf('django.db.models.fields.CharField')(max_length=30, default='4')),
            ('print_width', self.gf('django.db.models.fields.IntegerField')(default=30)),
            ('print_type', self.gf('django.db.models.fields.CharField')(max_length=30, default='print')),
            ('colour', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('catalogue', ['C2OProduct'])


    def backwards(self, orm):
        # Deleting model 'C2OProduct'
        db.delete_table('catalogue_c2oproduct')


    models = {
        'catalogue.c2oproduct': {
            'Meta': {'object_name': 'C2OProduct'},
            'colour': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'file_url': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'print_position': ('django.db.models.fields.CharField', [], {'max_length': '30', 'default': "'4'"}),
            'print_type': ('django.db.models.fields.CharField', [], {'max_length': '30', 'default': "'print'"}),
            'print_width': ('django.db.models.fields.IntegerField', [], {'default': '30'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'unique_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        }
    }

    complete_apps = ['catalogue']