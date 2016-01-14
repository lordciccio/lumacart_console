# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'C2OOrder'
        db.create_table('orders_c2oorder', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('luma_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('c2o_id', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_update', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now=True)),
            ('request_json', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=30, default='NEW')),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('delivery_method', self.gf('django.db.models.fields.CharField')(max_length=30, default='standard')),
            ('individual_bags', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('customer_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('customer_email', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('customer_telephone', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('address_delivery_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('address_company_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('address_address_line_1', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('address_address_line_2', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('address_city', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('address_county', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('address_postcode', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('address_country', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('orders', ['C2OOrder'])

        # Adding model 'C2OOrderItem'
        db.create_table('orders_c2oorderitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('quantity', self.gf('django.db.models.fields.IntegerField')()),
            ('size', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['orders.C2OOrder'])),
            ('c2o_sku', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal('orders', ['C2OOrderItem'])


    def backwards(self, orm):
        # Deleting model 'C2OOrder'
        db.delete_table('orders_c2oorder')

        # Deleting model 'C2OOrderItem'
        db.delete_table('orders_c2oorderitem')


    models = {
        'orders.c2oorder': {
            'Meta': {'object_name': 'C2OOrder'},
            'address_address_line_1': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'address_address_line_2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'address_city': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'address_company_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'address_country': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'address_county': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'address_delivery_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'address_postcode': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'c2o_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'customer_email': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'customer_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'customer_telephone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'delivery_method': ('django.db.models.fields.CharField', [], {'max_length': '30', 'default': "'standard'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'individual_bags': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'luma_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'request_json': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '30', 'default': "'NEW'"})
        },
        'orders.c2oorderitem': {
            'Meta': {'object_name': 'C2OOrderItem'},
            'c2o_sku': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['orders.C2OOrder']"}),
            'product_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        }
    }

    complete_apps = ['orders']