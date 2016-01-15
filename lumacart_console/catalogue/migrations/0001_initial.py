# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-15 09:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='C2OProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_id', models.CharField(max_length=255, unique=True)),
                ('sku_name', models.CharField(blank=True, max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('file_url', models.TextField(blank=True)),
                ('print_position', models.CharField(choices=[('1', 'Right Sleeve (max 10 cm)'), ('2', 'Bottom Right (max 12 cm)'), ('3', 'Right Chest\t (max 12 cm)'), ('4', 'Centre Chest (max 30 cm)'), ('5', 'Left Chest\t(max 12 cm)'), ('6', 'Bottom Left\t(max 12 cm)'), ('7', 'Left Sleeve\t(max 10 cm)'), ('8', 'Centre Back\t(max 30 cm)'), ('9', 'Top Back (max 30 cm)'), ('11', 'Front of Hat (max 8 cm)'), ('12', 'Bottom Back\t(max 30 cm)'), ('13', 'Front of Bag (max 30 cm)'), ('14', 'Centre Tea Towel (max 30 cm)'), ('15', 'Left Pocket\t(max 12 cm)'), ('16', 'Right Pocket (max 12 cm)'), ('17', 'Top Chest (max 30 cm)'), ('18', 'Inside Back (max 12 cm)'), ('19', 'Front of Tie (max 5 cm)')], default='4', max_length=30)),
                ('print_width', models.IntegerField(default=30)),
                ('print_type', models.CharField(choices=[('print', 'Print multi-colour'), ('print_1colour', 'Single-color print'), ('embroidery', 'Embroidery')], default='print', max_length=30)),
                ('colour', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='C2OSku',
            fields=[
                ('key', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('category', models.CharField(blank=True, max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('in_stock', models.BooleanField()),
                ('sku_code', models.CharField(max_length=255)),
                ('colour', models.CharField(max_length=255)),
                ('size', models.CharField(max_length=255)),
            ],
        ),
    ]
