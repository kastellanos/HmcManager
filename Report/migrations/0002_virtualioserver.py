# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-20 16:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Report', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VirtualIOServer',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('type', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('uuid', models.CharField(max_length=50)),
                ('associated_managed_system', models.CharField(max_length=50)),
                ('maximum_memory', models.FloatField()),
                ('desired_memory', models.FloatField()),
                ('minimum_memory', models.FloatField()),
                ('has_dedicated_processors', models.BooleanField()),
                ('maximum_processors', models.FloatField()),
                ('desired_processors', models.FloatField()),
                ('minimum_processors', models.FloatField()),
                ('maximum_processing_units', models.FloatField()),
                ('desired_processing_units', models.FloatField()),
                ('minimum_processing_units', models.FloatField()),
            ],
        ),
    ]
