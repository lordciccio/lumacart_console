# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-15 16:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20160115_1032'),
    ]

    operations = [
        migrations.AddField(
            model_name='c2oorder',
            name='est_dispatch_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='c2oorder',
            name='gross_order_value',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=19, null=True),
        ),
        migrations.AddField(
            model_name='c2oorder',
            name='net_order_value',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=19, null=True),
        ),
        migrations.AlterField(
            model_name='c2oorder',
            name='status',
            field=models.CharField(choices=[('NEW', 'NEW'), ('SENT', 'SENT'), ('INVALID', 'INVALID'), ('ERROR', 'ERROR'), ('DISPATCHED', 'DISPATCHED')], default='NEW', max_length=30),
        ),
        migrations.AlterField(
            model_name='c2oorderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='orders.C2OOrder'),
        ),
    ]
